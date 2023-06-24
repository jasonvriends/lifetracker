import { Routes } from '@angular/router';

export const routes: Routes = [

  // Default Layout
  // ===================================================================================

  { 
    path: '', 
    loadComponent : () => import('./layouts/default.component').then(c => c.DefaultComponent),
    children: [
      { path: '', loadComponent : () => import('./pages/dashboard.component').then(c => c.DashboardComponent), pathMatch: 'full'},
      { path: 'privacy', loadComponent : () => import('./pages/privacy.component').then(c => c.PrivacyComponent), pathMatch: 'full'},
    ]
  },
  
  // Full Screen Layout
  // ===================================================================================

  { 
    path: '', 
    loadComponent : () => import('./layouts/fullscreen.component').then(c => c.FullscreenComponent),
    children: [
      { path: '500', loadComponent : () => import('./pages/error500.component').then(c => c.Error500Component), pathMatch: 'full'},
      { path: '**', loadComponent : () => import('./pages/error404.component').then(c => c.Error404Component), pathMatch: 'full'},
    ]
  },

];

