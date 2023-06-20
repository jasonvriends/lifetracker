import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ColorschemeService {

  private isDarkModeSubject: BehaviorSubject<boolean>;
  public isDarkMode$: Observable<boolean>;

  constructor() {
    this.isDarkModeSubject = new BehaviorSubject<boolean>(this.getSavedTheme() ?? this.isSystemDarkMode());
    this.isDarkMode$ = this.isDarkModeSubject.asObservable();
    this.updateTheme();
  }

  toggleTheme(): void {
    const isDarkMode = !this.isDarkModeSubject.value;
    this.saveThemePreference(isDarkMode);
    this.isDarkModeSubject.next(isDarkMode);
    this.updateTheme();
  }

  updateTheme(): void {
    const themeClass = this.isDarkModeSubject.value ? 'dark' : 'light';
    document.body.setAttribute('data-bs-theme', themeClass);
  }

  isSystemDarkMode(): boolean {
    return window.matchMedia('(prefers-color-scheme: dark)').matches;
  }

  saveThemePreference(isDarkMode: boolean): void {
    localStorage.setItem('themePreference', JSON.stringify(isDarkMode));
  }

  getSavedTheme(): boolean | null {
    const themePreference = localStorage.getItem('themePreference');
    return themePreference ? JSON.parse(themePreference) : null;
  }
  
  updateDarkMode(isDarkMode: boolean): void {
    this.isDarkModeSubject.next(isDarkMode);
    this.updateTheme();
  }

}
