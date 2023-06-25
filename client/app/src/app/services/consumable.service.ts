import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { environment  } from '../../environments/environment';
import { AuthService } from '../services/auth.service';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ConsumableService {

  constructor(
    private http: HttpClient,
    private authService: AuthService
  ) { }

  fetchConsumableData(start_date: Date, end_date: Date): Observable<any> {
    
    const apiUrl = environment.apiUrl + 'consumable/';
    const utcStartDate = start_date.toUTCString();
    const utcEndDate = end_date.toUTCString();

    // Get the bearer token from AuthService
    const token = this.authService.accessToken;
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);

    // Construct the query parameters
    let params = new HttpParams();

    if (start_date && end_date) {
      params = params
        .set('start_date', start_date.toISOString())
        .set('end_date', end_date.toISOString());
    }

    return this.http.get(apiUrl, { headers, params });

  }

}
