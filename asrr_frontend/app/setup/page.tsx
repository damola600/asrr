"use client";

import {
  FormEvent,
  useEffect,
  useState,
} from "react";

import { useRouter } from "next/navigation";

import {
  API_BASE,
  apiFetch,
} from "@/lib/api";

import { countries } from "@/public/data/countries";


type SunnahPreferences = {
  tahajjud: boolean;
  duha: boolean;

  monday_fast: boolean;
  thursday_fast: boolean;
  white_days_fast: boolean;

  arafah_fast: boolean;
  ashura_fast: boolean;

  first_nine_dhul_hijjah: boolean;
  six_days_shawwal: boolean;

  surah_kahf_fri: boolean;

  friday_dua: boolean;
  friday_preparation: boolean;

  arafah_dua: boolean;

  morning_adhkar: boolean;
  evening_adhkar: boolean;

  surah_mulk_daily: boolean;
};


type SunnahOptionProps = {
  label: string;
  description?: string;
  checked: boolean;
  onChange: () => void;
};


const defaultSunnahPreferences: SunnahPreferences = {
  tahajjud: false,
  duha: false,

  monday_fast: false,
  thursday_fast: false,
  white_days_fast: false,

  arafah_fast: false,
  ashura_fast: false,

  first_nine_dhul_hijjah: false,
  six_days_shawwal: false,

  surah_kahf_fri: false,

  friday_dua: false,
  friday_preparation: false,

  arafah_dua: false,

  morning_adhkar: false,
  evening_adhkar: false,

  surah_mulk_daily: false,
};


const madhabs = [
  {
    value: "hanafi",
    label: "Hanafi",
  },
  {
    value: "shafi",
    label: "Shafi'i",
  },
  {
    value: "maliki",
    label: "Maliki",
  },
  {
    value: "hanbali",
    label: "Hanbali",
  },
  {
    value: "jaffari",
    label: "Ja'fari",
  },
];


export default function SetupPage() {

  const router = useRouter();


  // ------------------------------------
  // PROFILE STATE
  // ------------------------------------

  const [city, setCity] =
    useState("");

  const [country, setCountry] =
    useState("Canada");

  const [madhab, setMadhab] =
    useState("");


  // ------------------------------------
  // SUNNAH STATE
  // ------------------------------------

  const [
    sunnahEnabled,
    setSunnahEnabled,
  ] = useState(false);


  const [
    sunnahPreferences,
    setSunnahPreferences,
  ] = useState<SunnahPreferences>(
    defaultSunnahPreferences
  );


  // ------------------------------------
  // GOOGLE / SETUP STATE
  // ------------------------------------

  const [
    googleConnected,
    setGoogleConnected,
  ] = useState(false);


  const [
    profileSaved,
    setProfileSaved,
  ] = useState(false);


  const [
    checkingStatus,
    setCheckingStatus,
  ] = useState(true);


  // ------------------------------------
  // UI STATE
  // ------------------------------------

  const [
    saving,
    setSaving,
  ] = useState(false);


  const [
    error,
    setError,
  ] = useState("");


  const [
    message,
    setMessage,
  ] = useState("");


  // ------------------------------------
  // LOAD EXISTING SETUP
  // ------------------------------------

  useEffect(() => {
    loadExistingSetup();
  }, []);


  async function loadExistingSetup() {

    try {

      const [
        profileData,
        sunnahData,
      ] = await Promise.all([

        apiFetch(
          "/member/profile/"
        ),

        apiFetch(
          "/member/sunnah/"
        ),

      ]);


      // -------------------------------
      // PROFILE
      // -------------------------------

      setCity(
        profileData.city || ""
      );


      setCountry(
        profileData.country || "Canada"
      );


      setMadhab(
        profileData.madhab || ""
      );


      // -------------------------------
      // SUNNAH
      // -------------------------------

      setSunnahEnabled(
        sunnahData.sunnah_enabled ?? false
      );


      setSunnahPreferences({

        tahajjud:
          sunnahData.tahajjud ?? false,

        duha:
          sunnahData.duha ?? false,

        monday_fast:
          sunnahData.monday_fast ?? false,

        thursday_fast:
          sunnahData.thursday_fast ?? false,

        white_days_fast:
          sunnahData.white_days_fast ?? false,

        arafah_fast:
          sunnahData.arafah_fast ?? false,

        ashura_fast:
          sunnahData.ashura_fast ?? false,

        first_nine_dhul_hijjah:
          sunnahData.first_nine_dhul_hijjah
          ?? false,

        six_days_shawwal:
          sunnahData.six_days_shawwal
          ?? false,

        surah_kahf_fri:
          sunnahData.surah_kahf_fri
          ?? false,

        friday_dua:
          sunnahData.friday_dua
          ?? false,

        friday_preparation:
          sunnahData.friday_preparation
          ?? false,

        arafah_dua:
          sunnahData.arafah_dua
          ?? false,

        morning_adhkar:
          sunnahData.morning_adhkar
          ?? false,

        evening_adhkar:
          sunnahData.evening_adhkar
          ?? false,

        surah_mulk_daily:
          sunnahData.surah_mulk_daily
          ?? false,

      });


      // -------------------------------
      // GOOGLE
      // -------------------------------

      const connected =
        profileData
          .google_calendar_connected
        ?? false;


      setGoogleConnected(
        connected
      );


      // -------------------------------
      // ALREADY COMPLETE?
      // -------------------------------

      if (
        profileData.setup_complete &&
        connected
      ) {

        router.replace(
          "/dashboard"
        );

        return;
      }


      // -------------------------------
      // ALREADY SAVED ONCE?
      // -------------------------------

      if (
        profileData.city &&
        profileData.country &&
        profileData.madhab
      ) {

        setProfileSaved(
          true
        );
      }


    } catch {

      /*
       * If profile/sunnah cannot be
       * loaded, the session is probably
       * missing or expired.
       */

      router.replace(
        "/"
      );

    } finally {

      setCheckingStatus(
        false
      );
    }
  }


  // ------------------------------------
  // MARK FORM AS CHANGED
  // ------------------------------------

  function markUnsaved() {

    setProfileSaved(
      false
    );

    setMessage("");
  }


  // ------------------------------------
  // SUNNAH MASTER TOGGLE
  // ------------------------------------

  function handleSunnahToggle() {

    setSunnahEnabled(
      (current) => !current
    );

    /*
     * Do not clear the individual
     * Sunnah preferences.
     *
     * Turning the master toggle off
     * only disables/hides them.
     */

    markUnsaved();
  }


  // ------------------------------------
  // INDIVIDUAL SUNNAH OPTION
  // ------------------------------------

  function updateSunnahPreference(
    field: keyof SunnahPreferences
  ) {

    setSunnahPreferences(
      (current) => ({

        ...current,

        [field]:
          !current[field],

      })
    );

    markUnsaved();
  }


  // ------------------------------------
  // SAVE SETUP
  // ------------------------------------

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>
  ) {

    event.preventDefault();

    setError("");
    setMessage("");


    // -------------------------------
    // VALIDATION
    // -------------------------------

    if (!city.trim()) {

      setError(
        "Please enter your city."
      );

      return;
    }


    if (!country) {

      setError(
        "Please select your country."
      );

      return;
    }


    if (!madhab) {

      setError(
        "Please select your Madhab."
      );

      return;
    }


    setSaving(
      true
    );


    try {

      // -------------------------------
      // SAVE MEMBER PROFILE
      // -------------------------------

      /*
       * prayer_enabled is NOT sent here.
       *
       * New members use the backend
       * default:
       *
       * prayer_enabled = True
       *
       * They can later change it from
       * Dashboard -> Edit Preferences.
       */

      await apiFetch(
        "/member/profile/",
        {
          method: "PATCH",

          body: JSON.stringify({

            city:city.trim(),

            country,

            madhab,

          }),
        }
      );


      // -------------------------------
      // SAVE SUNNAH SETTINGS
      // -------------------------------

      await apiFetch(
        "/member/sunnah/",
        {
          method: "PATCH",

          body: JSON.stringify({

            sunnah_enabled:
              sunnahEnabled,

            ...sunnahPreferences,

          }),
        }
      );


      setProfileSaved(
        true
      );


      setMessage(
        "Preferences saved. Connect Google Calendar to finish setup."
      );


    } catch (error) {

      if (
        error instanceof Error
      ) {

        setError(
          error.message
        );

      } else {

        setError(
          "Something went wrong while saving your setup."
        );
      }


    } finally {

      setSaving(
        false
      );
    }
  }


  // ------------------------------------
  // GOOGLE
  // ------------------------------------

  function connectGoogle() {

    setError("");
    setMessage("");


    if (!profileSaved) {

      setError(
        "Please save your latest preferences before connecting Google Calendar."
      );

      return;
    }


    window.location.href =
      `${API_BASE}/user_event/google/connect/`;
  }


  // ------------------------------------
  // INITIAL LOADING
  // ------------------------------------

  if (checkingStatus) {

    return (

      <main className="setup-page">

        <section className="setup-card">

          <div className="loader">
            Loading your setup...
          </div>

        </section>

      </main>
    );
  }


  return (

    <main className="setup-page">

      <section className="setup-card">


        {/* --------------------------------
            HEADER
        -------------------------------- */}

        <header className="brand-header">

          <div className="moon-icon">
            ☾
          </div>


          <p className="eyebrow">
            ~ ASRR ~
          </p>


          <h1>
            Set up your calendar
          </h1>


          <p>
            Choose your location,
            Madhab and the Islamic
            reminders you want added
            to your calendar.
          </p>

        </header>


        {/* --------------------------------
            ERROR
        -------------------------------- */}

        {error && (

          <div className="error-message">
            {error}
          </div>

        )}


        {/* --------------------------------
            SUCCESS MESSAGE
        -------------------------------- */}

        {message && (

          <div className="status-message">
            {message}
          </div>

        )}


        <form
          className="auth-form"
          onSubmit={
            handleSubmit
          }
        >


          {/* ================================
              LOCATION
          ================================= */}

          <div className="setup-section">

            <div className="setup-section-header">

              <h2>
                Location
              </h2>


              <p>
                ASRR uses your location to
                calculate the correct
                prayer schedule.
              </p>

            </div>


            {/* CITY */}

            <div className="field-group">

              <label htmlFor="city">
                City
              </label>


              <input
                id="city"
                type="text"
                value={
                  city
                }
                onChange={(event) => {

                  setCity(
                    event.target.value
                  );

                  markUnsaved();

                }}
                placeholder="Guelph"
                autoComplete="address-level2"
                required
              />

            </div>


            {/* COUNTRY */}

            <div className="field-group">

              <label htmlFor="country">
                Country
              </label>


              <select
                id="country"
                value={
                  country
                }
                onChange={(event) => {

                  setCountry(
                    event.target.value
                  );

                  markUnsaved();

                }}
                required
              >

                <option value="">
                  Select your country
                </option>


                {countries.map(
                  (countryName) => (

                    <option
                      key={
                        countryName
                      }
                      value={
                        countryName
                      }
                    >
                      {countryName}
                    </option>

                  )
                )}

              </select>

            </div>


            {/* MADHAB */}

            <div className="field-group">

              <label htmlFor="madhab">
                Madhab
              </label>


              <select
                id="madhab"
                value={
                  madhab
                }
                onChange={(event) => {

                  setMadhab(
                    event.target.value
                  );

                  markUnsaved();

                }}
                required
              >

                <option value="">
                  Select your Madhab
                </option>


                {madhabs.map(
                  (item) => (

                    <option
                      key={
                        item.value
                      }
                      value={
                        item.value
                      }
                    >
                      {item.label}
                    </option>

                  )
                )}

              </select>

            </div>

          </div>


          {/* ================================
              SUNNAH
          ================================= */}

          <div
            className="
              setup-section
              sunnah-section
            "
          >

            <div className="setup-section-header">

              <h2>
                Sunnah Acts
              </h2>


              <p>
                Choose optional acts you
                would like ASRR to include
                in your calendar.
              </p>

            </div>


            {/* MASTER TOGGLE */}

            <label className="preference-card">

              <input
                type="checkbox"
                checked={
                  sunnahEnabled
                }
                onChange={
                  handleSunnahToggle
                }
              />


              <span>

                <strong>
                  Include Sunnah acts
                </strong>


                <small>
                  Add optional prayers,
                  fasting, Qur&apos;an and
                  remembrance reminders.
                </small>

              </span>

            </label>


            {/* SUNNAH OPTIONS */}

            {sunnahEnabled && (

              <div className="sunnah-options">

                <div className="sunnah-options-header">

                  <h3>
                    Choose your Sunnah acts
                  </h3>


                  <p>
                    Select the acts you
                    want included.
                  </p>

                </div>


                {/* ----------------------------
                    PRAYERS
                ---------------------------- */}

                <div className="sunnah-group">

                  <h3>
                    Prayers
                  </h3>


                  <SunnahOption
                    label="Tahajjud"
                    description="Reminder during the last third of the night."
                    checked={
                      sunnahPreferences
                        .tahajjud
                    }
                    onChange={() =>
                      updateSunnahPreference(
                        "tahajjud"
                      )
                    }
                  />


                  <SunnahOption
                    label="Duha"
                    description="Morning voluntary prayer reminder."
                    checked={
                      sunnahPreferences
                        .duha
                    }
                    onChange={() =>
                      updateSunnahPreference(
                        "duha"
                      )
                    }
                  />

                </div>


                {/* ----------------------------
                    FASTING
                ---------------------------- */}

                <div className="sunnah-group">

                  <h3>
                    Fasting
                  </h3>


                  <SunnahOption
                    label="Monday Fast"
                    checked={
                      sunnahPreferences
                        .monday_fast
                    }
                    onChange={() =>
                      updateSunnahPreference(
                        "monday_fast"
                      )
                    }
                  />


                  <SunnahOption
                    label="Thursday Fast"
                    checked={
                      sunnahPreferences
                        .thursday_fast
                    }
                    onChange={() =>
                      updateSunnahPreference(
                        "thursday_fast"
                      )
                    }
                  />


                  <SunnahOption
                    label="White Days"
                    description="13th, 14th and 15th of each Hijri month."
                    checked={
                      sunnahPreferences
                        .white_days_fast
                    }
                    onChange={() =>
                      updateSunnahPreference(
                        "white_days_fast"
                      )
                    }
                  />


                  <SunnahOption
                    label="Day of Arafah"
                    checked={
                      sunnahPreferences
                        .arafah_fast
                    }
                    onChange={() =>
                      updateSunnahPreference(
                        "arafah_fast"
                      )
                    }
                  />


                  <SunnahOption
                    label="Ashura"
                    checked={
                      sunnahPreferences
                        .ashura_fast
                    }
                    onChange={() =>
                      updateSunnahPreference(
                        "ashura_fast"
                      )
                    }
                  />


                  <SunnahOption
                    label="First Nine Days of Dhul Hijjah"
                    checked={
                      sunnahPreferences
                        .first_nine_dhul_hijjah
                    }
                    onChange={() =>
                      updateSunnahPreference(
                        "first_nine_dhul_hijjah"
                      )
                    }
                  />


                  <SunnahOption
                    label="Six Days of Shawwal"
                    checked={
                      sunnahPreferences
                        .six_days_shawwal
                    }
                    onChange={() =>
                      updateSunnahPreference(
                        "six_days_shawwal"
                      )
                    }
                  />

                </div>


                {/* ----------------------------
                    QURAN + ADHKAR
                ---------------------------- */}

                <div className="sunnah-group">

                  <h3>
                    Qur&apos;an &amp; Adhkar
                  </h3>


                  <SunnahOption
                    label="Morning Adhkar"
                    checked={
                      sunnahPreferences
                        .morning_adhkar
                    }
                    onChange={() =>
                      updateSunnahPreference(
                        "morning_adhkar"
                      )
                    }
                  />


                  <SunnahOption
                    label="Evening Adhkar"
                    checked={
                      sunnahPreferences
                        .evening_adhkar
                    }
                    onChange={() =>
                      updateSunnahPreference(
                        "evening_adhkar"
                      )
                    }
                  />


                  <SunnahOption
                    label="Surah Al-Mulk"
                    description="Daily reminder."
                    checked={
                      sunnahPreferences
                        .surah_mulk_daily
                    }
                    onChange={() =>
                      updateSunnahPreference(
                        "surah_mulk_daily"
                      )
                    }
                  />


                  <SunnahOption
                    label="Surah Al-Kahf"
                    description="Friday reminder."
                    checked={
                      sunnahPreferences
                        .surah_kahf_fri
                    }
                    onChange={() =>
                      updateSunnahPreference(
                        "surah_kahf_fri"
                      )
                    }
                  />

                </div>


                {/* ----------------------------
                    SPECIAL REMINDERS
                ---------------------------- */}

                <div className="sunnah-group">

                  <h3>
                    Special Reminders
                  </h3>


                  <SunnahOption
                    label="Friday Du'a"
                    checked={
                      sunnahPreferences
                        .friday_dua
                    }
                    onChange={() =>
                      updateSunnahPreference(
                        "friday_dua"
                      )
                    }
                  />


                  <SunnahOption
                    label="Friday Preparation"
                    checked={
                      sunnahPreferences
                        .friday_preparation
                    }
                    onChange={() =>
                      updateSunnahPreference(
                        "friday_preparation"
                      )
                    }
                  />


                  <SunnahOption
                    label="Arafah Du'a"
                    checked={
                      sunnahPreferences
                        .arafah_dua
                    }
                    onChange={() =>
                      updateSunnahPreference(
                        "arafah_dua"
                      )
                    }
                  />

                </div>

              </div>

            )}

          </div>


          {/* ================================
              SAVE
          ================================= */}

          <div className="setup-section">

            <button
              type="submit"
              className="primary-button"
              disabled={
                saving
              }
            >

              {
                saving
                  ? "Saving..."
                  : profileSaved
                    ? "Preferences Saved"
                    : "Save Preferences"
              }

            </button>

          </div>


          {/* ================================
              GOOGLE
          ================================= */}

          <div
            className="
              google-setup-card
              required-google
            "
          >

            <div>

              <div className="google-title-row">

                <strong>
                  Google Calendar
                </strong>


                <span className="required-badge">
                  Required
                </span>

              </div>


              <p>
                Connect Google Calendar to
                finish setting up ASRR and
                synchronize your prayer
                schedule and reminders.
              </p>

            </div>


            {googleConnected ? (

              <span className="connected-badge">
                ✓ Connected
              </span>

            ) : (

              <button
                type="button"
                className="secondary-button"
                disabled={
                  !profileSaved ||
                  saving
                }
                onClick={
                  connectGoogle
                }
              >
                Connect Google Calendar
              </button>

            )}

          </div>


          {!profileSaved && (

            <p className="setup-helper">
              Save your latest preferences
              before connecting Google
              Calendar.
            </p>

          )}


          {profileSaved &&
            !googleConnected && (

            <p className="setup-helper">
              Your preferences are saved.
              Connect Google Calendar to
              complete setup.
            </p>

          )}

        </form>

      </section>

    </main>
  );
}


/* ==========================================
   REUSABLE SUNNAH OPTION
========================================== */

function SunnahOption({
  label,
  description,
  checked,
  onChange,
}: SunnahOptionProps) {

  return (

    <label className="sunnah-option">

      <input
        type="checkbox"
        checked={
          checked
        }
        onChange={
          onChange
        }
      />


      <span>

        <strong>
          {label}
        </strong>


        {description && (

          <small>
            {description}
          </small>

        )}

      </span>

    </label>
  );
}