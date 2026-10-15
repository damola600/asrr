'use client';

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { login } from "./auth/login";
import { register } from "./auth/register";
import './page.module.css';

export default function Landing(){
  const router = useRouter();

  // States 
  const [mode, setMode] = useState<'login' | 'signup'>('login');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [loginEmail, setLoginEmail] = useState("");
  const [loginPassword, setLoginPassword] = useState("");

  const [signupEmail, setSignupEmail] = useState("");
  const [signupPassword, setSignupPassword] = useState("");

  // Login Function
  async function handleLogin(event: FormEvent<HTMLFormElement>){
    event.preventDefault();
    setError("");
    setLoading(true);

    try{
      const data = await login(loginEmail, loginPassword);

      

      if (data.setup_complete && data.google_calendar_connected){
        router.push('/dashboard');
      }else {
        router.push('/setup');
      }
    }catch(error){
      if (error instanceof Error){
        setError(error.message);
      }else{
        setError('Unable to sign in');
      }
    }finally{
      setLoading(false);
      setLoginEmail("");
      setLoginPassword("");
    }
  };

  async function handleRegister(event: FormEvent<HTMLFormElement>){
    event.preventDefault();

    setError("");
    setLoading(true);

    try{
      await register(signupEmail, signupPassword);

      // setSignupEmail("");
      // setSignupPassword("");

      router.push('/setup');
    }catch(error){
      if (error instanceof Error){
        setError(error.message);
      }else {
        setError('Unable to create account');
      }
    }finally{
      setLoading(false);
      setSignupEmail("");
      setSignupPassword("");
    }
  };

  return (
    <main className="auth-page">
      <div className="background-overlay" />

      <section className="auth-card">
        <header className="brand-header">
          <div className="moon-icon">☾</div>
          <h1 className="brand-name">~ ASRR ~</h1>
          <p className="brand-description">Your personal islamic calendar for prayer, remembrance and sunnah</p>
        </header>

       {/* <div className="auth-tabs">
          <button 
          type="button" 
          className={mode === 'login' ? 'auth-tab active':'auth-tab'} 
          onClick={()=>{setMode('login'); setError("");}}>Sign In</button>
          <button
          type="button" 
          className={mode === 'login' ? 'auth-tab active':'auth-tab'} 
          onClick={()=>{setMode('login'); setError("");}}>Create Account</button>
        </div> */}

        {error && (
          <div className="error-message">{error}</div>
        )}

        {mode === 'login' ? (
          <form className="auth-form" onSubmit={handleLogin}>
            <div className="field-group">
              <label htmlFor="loginEmail">Email</label>
              <input id="loginEmail" type="email" value={loginEmail} onChange={(event)=>setLoginEmail(event.target.value)}
              placeholder="johndoe@example.com" autoComplete="email" required />
            </div>
            <div className="field-group">
              <label htmlFor="loginPassword">Password</label>
              <input id="loginPassword" type="password" value={loginPassword} onChange={(event)=>setLoginPassword(event.target.value)}
              placeholder="password" autoComplete="current-password" required />
            </div>

            <button className="primary-button" type="submit" disabled={loading}>{loading ? "Signing in..." : "Sign In"}</button>
            <p className="auth-switch">Don&apos;t have an account?{" "}
            <button type="button" onClick={()=>{setMode("signup"); setError("");}}>Sign up</button></p>
          </form>
        ): (
          <form className="auth-form" onSubmit={handleRegister}>
            <div className="field-group">
              <label htmlFor="signupEmail">Email</label>
              <input id="signupEmail" type="email" value={signupEmail} onChange={(event)=>setSignupEmail(event.target.value)}
              placeholder="johndoe@example.com" autoComplete="email" required />
            </div>
            <div className="field-group">
              <label htmlFor="signupPassword">Password</label>
              <input id="signupPassword" type="password" value={signupPassword} onChange={(event)=>setSignupPassword(event.target.value)}
              placeholder="At least 8 characters" autoComplete="new-password" required />
            </div>
            <button className="primary-button" type="submit" disabled={loading}>{loading ? "Creating account..." : "Create Account"}</button>
            <p className="auth-switch">
              Already have an account?{" "}
              <button type="button" onClick={()=>{setMode("login"); setError("");}}>Sign in</button>
            </p>
          </form>
        )}
      </section>
    </main>
  )


}