import { Routes } from '@angular/router';

export const routes: Routes = [

  // Default layout
  { 
    path: '', 
    loadComponent : () => import('../app/layouts/default.component').then(c => c.DefaultComponent),
    children: [
      { path: '', loadComponent : () => import('../app/pages/home.component').then(c => c.HomeComponent), pathMatch: 'full'},
      { path: 'dashboard', loadComponent : () => import('../app/pages/dashboard.component').then(c => c.DashboardComponent), pathMatch: 'full'},
      { path: 'about', loadComponent : () => import('../app/pages/about.component').then(c => c.AboutComponent), pathMatch: 'full'},
      { path: 'privacy', loadComponent : () => import('../app/pages/privacy.component').then(c => c.PrivacyComponent), pathMatch: 'full'},
    ]
  },
  
  // Fullpage layout
  { 
    path: '**', 
    loadComponent : () => import('../app/layouts/fullpage.component').then(c => c.FullpageComponent),
    children: [
      { path: '**', loadComponent : () => import('../app/pages/pagenotfound.component').then(c => c.PagenotfoundComponent), pathMatch: 'full'},
    ]
  },

];

