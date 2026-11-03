'use client';

import { apiFetch } from '@/lib/api';

export async function getCSRF() {
    try{
        const csrfResponse = await apiFetch(`/member/csrf/`,
            {
                credentials: "include",
            }
        );

        if (!csrfResponse.ok) {
        throw new Error("Unable to initialize CSRF protection");
        }

        const data = csrfResponse.json().csrfToken;

        const csrfToken = data.csrfToken ?? data.csrf_token;

        if(typeof csrfToken !== 'string' || !csrfToken){
            throw new Error('CSRF token missing from response');
        }
        
        return csrfToken;
    }
    catch (error){
        console.error(`Unable to get CSRF token: ${error}`);
        
        return {'message':  `Error: ${error}`};
    }
    
}

