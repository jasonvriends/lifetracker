import { Routes } from '@angular/router';

export const routes: Routes = [

  { 
    path: '', 
    loadComponent : () => import('./layouts/default.component').then(c => c.DefaultComponent),
    children: [
      { path: '', loadComponent : () => import('./pages/dashboard.component').then(c => c.DashboardComponent), pathMatch: 'full'},
    ]
  },
  
];

