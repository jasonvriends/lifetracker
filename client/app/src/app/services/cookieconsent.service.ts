import { Injectable } from '@angular/core';
import { tap } from 'rxjs/operators';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CookieConsentService {
  private readonly consentStatusKey = 'cookieConsentStatus';
  private consentStatusSubject = new BehaviorSubject<boolean>(false);

  constructor() {
    const consentStatus = this.getConsentStatusFromLocalStorage();
    this.consentStatusSubject.next(consentStatus);
  }

  hasConsented(): boolean {
    return this.getConsentStatusFromLocalStorage();
  }

  getConsentStatus(): BehaviorSubject<boolean> {
    return this.consentStatusSubject;
  }

  setConsent(consent: boolean) {
    this.saveConsentStatusToLocalStorage(consent);
    this.consentStatusSubject.next(consent);
    console.log('Cookie consent status saved to local storage');
  }

  private getConsentStatusFromLocalStorage(): boolean {
    const consentStatus = localStorage.getItem(this.consentStatusKey);
    return consentStatus === 'true';
  }

  private saveConsentStatusToLocalStorage(consent: boolean) {
    localStorage.setItem(this.consentStatusKey, consent.toString());
  }
}
