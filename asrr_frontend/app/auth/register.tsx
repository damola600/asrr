'use client';

import { useState } from 'react';
import { apiFetch } from '@/lib/api';
import { verifySession } from './session';

export async function register(email: string, password: string){
    const normalizedEmail = email.trim().toLowerCase();

    const data = await apiFetch('/member/register/', {
        method: 'POST',
        body: JSON.stringify({
            email: normalizedEmail,
            password,
        }),
    });

    const inSession = await verifySession();
    
    if(!inSession){
        throw new Error('Your account was created, but the browser could not establish a session.');
    }

    return data;
}