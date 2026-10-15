'use client';

import { useState } from 'react';
import { apiFetch } from '@/lib/api';

export async function verifySession(){
    try{
        await apiFetch('/member/profile', {
            method: 'GET',
        });
        return true;
    }catch (error){
        console.error(`Session verification failed: ${error}`);
        
        return false;
    }
}