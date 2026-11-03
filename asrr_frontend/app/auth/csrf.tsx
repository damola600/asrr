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

        return csrfResponse.json();
    }
    catch (error){
        console.error(`Unable to get CSRF token: ${error}`);
        
        return {'message':  `Error: ${error}`};
    }
    
}

