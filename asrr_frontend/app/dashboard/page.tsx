"use client";

import {
  FormEvent,
  useEffect,
  useState,
} from "react";

import {
  useRouter,
} from "next/navigation";

import {
  API_BASE,
  apiFetch,
} from "@/lib/api";

import {
  countries,
} from "@/public/data/countries";

import "./page.module.css";


type UserProfile = {
  email: string;

  google_cal_email:
  string | null;

  city: string;
  country: string;
  madhab: string;

  prayer_enabled: boolean;

  setup_complete: boolean;

  google_calendar_connected:
  boolean;
};


type SunnahPreferences = {
  sunnah_enabled: boolean;

  tahajjud: boolean;
  duha: boolean;

  monday_fast: boolean;
  thursday_fast: boolean;
  white_days_fast: boolean;

  arafah_fast: boolean;
  ashura_fast: boolean;

  first_nine_dhul_hijjah:
  boolean;

  six_days_shawwal:
  boolean;

  surah_kahf_fri:
  boolean;

  friday_dua:
  boolean;

  friday_preparation:
  boolean;

  arafah_dua:
  boolean;

  morning_adhkar:
  boolean;

  evening_adhkar:
  boolean;

  surah_mulk_daily:
  boolean;
};


type SunnahOptionProps = {
  label: string;
  description?: string;
  checked: boolean;
  onChange: () => void;
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


export default function Dashboard() {

  const router =
    useRouter();


  // ====================================
  // SAVED BACKEND DATA
  // ====================================

  const [
    profile,
    setProfile,
  ] =
    useState<UserProfile | null>(
      null
    );


  const [
    sunnah,
    setSunnah,
  ] =
    useState<SunnahPreferences | null>(
      null
    );


  // ====================================
  // EDIT FORM STATE
  // ====================================

  const [
    editMode,
    setEditMode,
  ] =
    useState(false);


  const [
    editCity,
    setEditCity,
  ] =
    useState("");


  const [
    editCountry,
    setEditCountry,
  ] =
    useState("");


  const [
    editMadhab,
    setEditMadhab,
  ] =
    useState("");


  const [
    editPrayerEnabled,
    setEditPrayerEnabled,
  ] =
    useState(true);


  const [
    editSunnah,
    setEditSunnah,
  ] =
    useState<SunnahPreferences | null>(
      null
    );


  // ====================================
  // UI STATE
  // ====================================

  const [
    loading,
    setLoading,
  ] =
    useState(true);


  const [
    saving,
    setSaving,
  ] =
    useState(false);


  const [
    message,
    setMessage,
  ] =
    useState("");


  const [
    error,
    setError,
  ] =
    useState("");


  // ====================================
  // LOAD DASHBOARD
  // ====================================

  useEffect(() => {
    loadDashboard();
  }, []);


  async function loadDashboard() {

    try {

      const [
        profileData,
        sunnahData,
      ] =
        await Promise.all([

          apiFetch(
            "/member/profile/"
          ),

          apiFetch(
            "/member/sunnah/"
          ),

        ]);


      if (
        !profileData.setup_complete ||
        !profileData
          .google_calendar_connected
      ) {

        router.replace(
          "/setup"
        );

        return;
      }


      setProfile(
        profileData
      );


      setSunnah(
        sunnahData
      );

    } catch (error) {

      console.error(
        "Dashboard load error:",
        error
      );

      router.replace(
        "/"
      );

    } finally {

      setLoading(
        false
      );
    }
  }


  // ====================================
  // ENTER EDIT MODE
  // ====================================

  function startEditing() {

    if (
      !profile ||
      !sunnah
    ) {
      return;
    }


    setEditCity(
      profile.city
    );

    setEditCountry(
      profile.country
    );

    setEditMadhab(
      profile.madhab
    );


    // Load the saved prayer preference
    // into the edit form.
    setEditPrayerEnabled(
      profile.prayer_enabled
    );


    setEditSunnah({
      ...sunnah,
    });


    setMessage("");
    setError("");

    setEditMode(
      true
    );
  }


  // ====================================
  // CANCEL EDIT
  // ====================================

  function cancelEditing() {

    setEditMode(
      false
    );

    setEditSunnah(
      null
    );

    setError("");
  }


  // ====================================
  // EDIT SUNNAH OPTION
  // ====================================

  function updateSunnahPreference(
    field: keyof SunnahPreferences
  ) {

    if (!editSunnah) {
      return;
    }


    setEditSunnah({
      ...editSunnah,

      [field]:
        !editSunnah[field],
    });
  }


  // ====================================
  // SAVE ALL PREFERENCES
  // ====================================

  async function savePreferences(
    event: FormEvent<HTMLFormElement>
  ) {

    event.preventDefault();


    if (
      !profile ||
      !editSunnah
    ) {
      return;
    }


    setError("");
    setMessage("");


    if (!editCity.trim()) {

      setError(
        "Please enter your city."
      );

      return;
    }


    if (!editCountry) {

      setError(
        "Please select your country."
      );

      return;
    }


    if (!editMadhab) {

      setError(
        "Please select your Madhab."
      );

      return;
    }


    setSaving(
      true
    );


    try {

      // ==================================
      // SAVE PROFILE FIRST
      // ==================================
      //
      // This includes prayer_enabled.
      //
      // We save this before Sunnah instead
      // of running both PATCH requests at
      // the same time. This prevents two
      // calendar refreshes from competing.

      const profileResult =
        await apiFetch(
          "/member/profile/",
          {
            method: "PATCH",
            body: JSON.stringify({
              city: editCity.trim(),
              country: editCountry,
              madhab: editMadhab,
              prayer_enabled: editPrayerEnabled,

            }),
          }
        );


      // ==================================
      // SAVE SUNNAH SECOND
      // ==================================

      const sunnahResult =
        await apiFetch(
          "/member/sunnah/",
          {
            method: "PATCH",
            body: JSON.stringify(editSunnah),
          }
        );


      // ==================================
      // UPDATE SAVED FRONTEND STATE
      // ==================================

      setProfile({
        ...profile,
        ...profileResult.profile,
        prayer_enabled:
          profileResult.profile
            ?.prayer_enabled
          ??
          editPrayerEnabled,

        google_calendar_connected:
          profile
            .google_calendar_connected,
      });


      setSunnah(
        sunnahResult.preferences
      );


      setEditMode(
        false
      );


      setMessage(
        "Preference Saved. Your Google Calendar is being updated."
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
          "Unable to save your preferences."
        );
      }

    } finally {

      setSaving(
        false
      );
    }
  }


  // ====================================
  // LOGOUT
  // ====================================

  async function logout() {

    try {

      await apiFetch(
        "/member/logout/",
        {
          method:
            "POST",
        }
      );

    } finally {

      router.replace(
        "/"
      );
    }
  }


  // ====================================
  // GOOGLE CONNECT
  // ====================================

  function connectGoogle() {

    window.location.href =
      `${API_BASE}/user_event/google/connect/`;
  }


  // ====================================
  // LOADING
  // ====================================

  if (loading) {

    return (
      <main className="dashboard-page">

        <div className="loader">
          Loading your calendar...
        </div>

      </main>
    );
  }


  if (
    !profile ||
    !sunnah
  ) {

    return null;
  }


  // ====================================
  // PAGE
  // ====================================

  return (

    <main className="dashboard-page">

      <div
        className="dashboard-overlay"
      />


      <div
        className="dashboard-shell"
      >


        {/* ==============================
            HEADER
        ============================== */}

        <header
          className="dashboard-header"
        >

          <div>

            <p className="eyebrow">
              ~ ASRR ~
            </p>

            <h1>
              Your Calendar
            </h1>

            <p>
              Your Islamic calendar
              preferences and connections.
            </p>

          </div>


          <div className="dashboard-header-actions">

            {!editMode && (

              <button
                type="button"
                className="primary-button"
                onClick={
                  startEditing
                }
              >
                Edit Preferences
              </button>

            )}


            <button
              type="button"
              className="secondary-button"
              onClick={
                logout
              }
            >
              Log Out
            </button>

          </div>

        </header>


        {/* ==============================
            MESSAGES
        ============================== */}

        {message && (

          <div className="status-message">
            {message}
          </div>

        )}


        {error && (

          <div className="error-message">
            {error}
          </div>

        )}


        {/* ==================================
            EDIT MODE
        ================================== */}

        {editMode &&
          editSunnah && (

            <form
              className="preferences-editor"
              onSubmit={
                savePreferences
              }
            >

              <div className="editor-header">

                <div>

                  <h2>
                    Edit Preferences
                  </h2>

                  <p>
                    Changes to your
                    location, Madhab,
                    prayer or Sunnah
                    settings will update
                    your calendar.
                  </p>

                </div>

              </div>


              {/* ============================
                LOCATION
            ============================ */}

              <section
                className="editor-section"
              >

                <h3>
                  Location
                </h3>


                <div className="field-group">

                  <label htmlFor="edit-city">
                    City
                  </label>

                  <input
                    id="edit-city"
                    type="text"
                    value={
                      editCity
                    }
                    onChange={
                      (event) =>
                        setEditCity(
                          event.target.value
                        )
                    }
                    required
                  />

                </div>


                <div className="field-group">

                  <label htmlFor="edit-country">
                    Country
                  </label>

                  <select
                    id="edit-country"
                    value={
                      editCountry
                    }
                    onChange={
                      (event) =>
                        setEditCountry(
                          event.target.value
                        )
                    }
                    required
                  >

                    <option value="">
                      Select country
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


                <div className="field-group">

                  <label htmlFor="edit-madhab">
                    Madhab
                  </label>

                  <select
                    id="edit-madhab"
                    value={
                      editMadhab
                    }
                    onChange={
                      (event) =>
                        setEditMadhab(
                          event.target.value
                        )
                    }
                    required
                  >

                    <option value="">
                      Select Madhab
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

              </section>


              {/* ============================
                DAILY PRAYERS
            ============================ */}

              <section
                className="editor-section"
              >

                <h3>
                  Daily Prayers
                </h3>


                <label
                  className="preference-card"
                >

                  <input
                    type="checkbox"
                    checked={
                      editPrayerEnabled
                    }
                    onChange={() =>
                      setEditPrayerEnabled(
                        (current) =>
                          !current
                      )
                    }
                  />


                  <span>

                    <strong>
                      Include daily prayers
                    </strong>

                    <small>
                      Add Fajr, Dhuhr, Asr,
                      Maghrib and Isha to
                      your Google Calendar.
                    </small>

                  </span>

                </label>

              </section>


              {/* ============================
                SUNNAH
            ============================ */}

              <section
                className="editor-section"
              >

                <h3>
                  Sunnah Acts
                </h3>


                <label
                  className="preference-card"
                >

                  <input
                    type="checkbox"
                    checked={
                      editSunnah
                        .sunnah_enabled
                    }
                    onChange={() =>
                      updateSunnahPreference(
                        "sunnah_enabled"
                      )
                    }
                  />


                  <span>

                    <strong>
                      Include Sunnah acts
                    </strong>

                    <small>
                      Enable or disable
                      your optional Islamic
                      reminders.
                    </small>

                  </span>

                </label>


                {editSunnah
                  .sunnah_enabled && (

                    <div
                      className="sunnah-options"
                    >

                      {/* PRAYERS */}

                      <div
                        className="sunnah-group"
                      >

                        <h4>
                          Prayers
                        </h4>


                        <SunnahOption
                          label="Tahajjud"
                          checked={
                            editSunnah
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
                          checked={
                            editSunnah
                              .duha
                          }
                          onChange={() =>
                            updateSunnahPreference(
                              "duha"
                            )
                          }
                        />

                      </div>


                      {/* FASTING */}

                      <div
                        className="sunnah-group"
                      >

                        <h4>
                          Fasting
                        </h4>


                        <SunnahOption
                          label="Monday Fast"
                          checked={
                            editSunnah
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
                            editSunnah
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
                            editSunnah
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
                            editSunnah
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
                            editSunnah
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
                            editSunnah
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
                            editSunnah
                              .six_days_shawwal
                          }
                          onChange={() =>
                            updateSunnahPreference(
                              "six_days_shawwal"
                            )
                          }
                        />

                      </div>


                      {/* QURAN + ADHKAR */}

                      <div
                        className="sunnah-group"
                      >

                        <h4>
                          Qur&apos;an &amp; Adhkar
                        </h4>


                        <SunnahOption
                          label="Morning Adhkar"
                          checked={
                            editSunnah
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
                            editSunnah
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
                          checked={
                            editSunnah
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
                          checked={
                            editSunnah
                              .surah_kahf_fri
                          }
                          onChange={() =>
                            updateSunnahPreference(
                              "surah_kahf_fri"
                            )
                          }
                        />

                      </div>


                      {/* SPECIAL */}

                      <div
                        className="sunnah-group"
                      >

                        <h4>
                          Special Reminders
                        </h4>


                        <SunnahOption
                          label="Friday Du'a"
                          checked={
                            editSunnah
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
                            editSunnah
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
                            editSunnah
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

              </section>


              {/* ============================
                SAVE / CANCEL
            ============================ */}

              <div
                className="editor-actions"
              >

                <button
                  type="button"
                  className="secondary-button"
                  onClick={
                    cancelEditing
                  }
                  disabled={
                    saving
                  }
                >
                  Cancel
                </button>


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
                      : "Save Changes"
                  }
                </button>

              </div>

            </form>

          )}


        {/* ==================================
            NORMAL DASHBOARD
        ================================== */}

        {!editMode && (

          <section
            className="dashboard-grid"
          >


            {/* LOCATION */}

            <article
              className="dashboard-card"
            >

              <span className="card-icon">
                ◷
              </span>


              <h2>
                Location
              </h2>


              <p className="big-value">
                {profile.city}
              </p>


              <p>
                {profile.country}
              </p>


              <div className="detail-row">

                <span>
                  Madhab
                </span>

                <strong>
                  {
                    formatMadhab(
                      profile.madhab
                    )
                  }
                </strong>

              </div>

            </article>


            {/* DAILY PRAYERS */}

            <article
              className="dashboard-card"
            >

              <span className="card-icon">
                ◷
              </span>


              <h2>
                Daily Prayers
              </h2>


              <p>
                Fajr, Dhuhr, Asr,
                Maghrib and Isha
                prayer times.
              </p>


              <div className="detail-row">

                <span>
                  Status
                </span>

                <strong>
                  {
                    profile.prayer_enabled
                      ? "Enabled"
                      : "Disabled"
                  }
                </strong>

              </div>

            </article>


            {/* SUNNAH */}

            <article
              className="dashboard-card"
            >

              <span className="card-icon">
                ☾
              </span>


              <h2>
                Sunnah Acts
              </h2>


              <p>
                Optional Sunnah acts and
                fasting reminders.
              </p>


              <div className="detail-row">

                <span>
                  Status
                </span>

                <strong>
                  {
                    sunnah.sunnah_enabled
                      ? "Enabled"
                      : "Disabled"
                  }
                </strong>

              </div>


              {sunnah.sunnah_enabled && (

                <p>
                  {
                    countSelectedSunnah(
                      sunnah
                    )
                  } selected reminders
                </p>

              )}

            </article>


            {/* GOOGLE */}

            <article
              className="
                dashboard-card
                google-card
              "
            >

              <span className="card-icon">
                ◉
              </span>


              <h2>
                Google Calendar
              </h2>


              {
                profile
                  .google_calendar_connected
                  ? (

                    <>

                      <div
                        className="connected-badge"
                      >
                        ✓ Connected
                      </div>


                      <p>
                        ASRR can synchronize
                        prayer times and your
                        selected Islamic
                        reminders.
                      </p>

                    </>

                  ) : (

                    <>

                      <div
                        className="not-connected-badge"
                      >
                        Not connected
                      </div>


                      <button
                        type="button"
                        className="primary-button"
                        onClick={
                          connectGoogle
                        }
                      >
                        Connect Google Calendar
                      </button>

                    </>

                  )}

            </article>


            {/* ACCOUNT */}

            <article
              className="dashboard-card"
            >

              <span className="card-icon">
                ✦
              </span>


              <h2>
                Account
              </h2>


              <div className="detail-row">

                <span>
                  Email
                </span>

                <strong>
                  {profile.email}
                </strong>

              </div>


              <div className="detail-row">

                <span>
                  Calendar
                </span>

                <strong>
                  {
                    profile
                      .google_cal_email
                    ??
                    "Google Calendar connected"
                  }
                </strong>

              </div>

            </article>

          </section>

        )}

      </div>

    </main>
  );
}


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


function formatMadhab(
  madhab: string
) {

  const labels:
    Record<string, string> = {

    hanafi: "Hanafi",
    shafi: "Shafi'i",
    maliki: "Maliki",
    hanbali: "Hanbali",
    jaffari: "Ja'fari",

  };


  return (
    labels[madhab] ??
    madhab
  );
}


function countSelectedSunnah(
  sunnah: SunnahPreferences
) {

  const {
    sunnah_enabled,
    ...preferences
  } = sunnah;


  return Object.values(
    preferences
  ).filter(Boolean).length;
}