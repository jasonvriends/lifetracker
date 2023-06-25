import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import Litepicker from 'litepicker';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { AuthService } from '../services/auth.service';
import { environment  } from '../../environments/environment';
import { ConsumableService } from '../services/consumable.service';

@Component({
  selector: 'page-dashboard',
  standalone: true,
  imports: [CommonModule],
  template: `
  
    <!-- Page header -->
    <div class="page-header d-print-none">
      
      <!-- container-xl -->  
      <div class="container-xl">
        
        <!-- row g-2 align-items-center -->
        <div class="row g-2 align-items-center">

          <!-- col -->
          <div class="col">
            <h2 class="page-title">
              Dashboard
            </h2>
          </div>
          <!-- col -->

          <!-- col -->
          <div class="col">
            <div class="row g-2 align-items-center">
              <div class="col-6 col-sm-4 col-md-2 col-xl-auto py-3">
                <a href="#" class="btn btn-pill w-150" id="datepicker">
                    {{ activity_date | date: 'MMMM d, yyy' }}
                </a>
              </div>
            </div>
          </div>
        <!-- col -->

        <!-- Page title actions -->
        <div class="col-auto ms-auto d-print-none">

          <div class="btn-list">
            <a href="#" class="btn btn-primary d-none d-sm-inline-block" data-bs-toggle="modal" data-bs-target="#modal-report">
              <!-- Download SVG icon from http://tabler-icons.io/i/plus -->
              <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M12 5l0 14"></path><path d="M5 12l14 0"></path></svg>
              Consumable
            </a>
            <a href="#" class="btn btn-primary d-sm-none btn-icon" data-bs-toggle="modal" data-bs-target="#modal-report" aria-label="Create new report">
              <!-- Download SVG icon from http://tabler-icons.io/i/plus -->
              <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M12 5l0 14"></path><path d="M5 12l14 0"></path></svg>
            </a>
          </div>        

        </div>

      </div>

    </div>

    <!-- Page content -->
    <div class="page-body">
      <div class="container-xl">
        <div class="row justify-content-center">
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">Activity</h3>
            </div>
            <div class="list-group list-group-flush list-group-hoverable">
              <div class="list-group-item">
                <div class="row align-items-center">
                  <div class="col-auto">
                    <span class="d-block text-muted text-truncate mt-n1">8:30 AM</span>
                  </div>
                  <div class="col-auto">
                      <span class="avatar">
                        <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-tools-kitchen-2" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                          <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                          <path d="M19 3v12h-5c-.023 -3.681 .184 -7.406 5 -12zm0 12v6h-1v-3m-10 -14v17m-3 -17v3a3 3 0 1 0 6 0v-3"></path>
                        </svg>
                      </span>
                  </div>
                  <div class="col text-truncate">
                    <span class="text-reset d-block">Keto Breakfast</span>
                    <div class="d-block text-muted text-truncate mt-n1">3 eggs with 6 slices of bacon and side of tomatoes</div>
                  </div>
          
                  <div class="col-auto">
                    <div class="list-inline-item">
                      <span>
                        <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-point-filled" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                          <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                          <path d="M12 7a5 5 0 1 1 -4.995 5.217l-.005 -.217l.005 -.217a5 5 0 0 1 4.995 -4.783z" stroke-width="0" fill="currentColor"></path>
                        </svg>
                        Eggs
                      </span>
                      <span>
                        <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-point-filled" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                          <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                          <path d="M12 7a5 5 0 1 1 -4.995 5.217l-.005 -.217l.005 -.217a5 5 0 0 1 4.995 -4.783z" stroke-width="0" fill="currentColor"></path>
                        </svg>
                        Bacon
                      </span>
                      <span>
                        <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-point-filled" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                          <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                          <path d="M12 7a5 5 0 1 1 -4.995 5.217l-.005 -.217l.005 -.217a5 5 0 0 1 4.995 -4.783z" stroke-width="0" fill="currentColor"></path>
                        </svg>
                        Tomatoes
                      </span>                                            
                    </div>
                  </div>

                  <div class="col-auto">
                    <a href="#" class="list-group-item-actions">
                      <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-pencil" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                        <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                        <path d="M4 20h4l10.5 -10.5a1.5 1.5 0 0 0 -4 -4l-10.5 10.5v4"></path>
                        <path d="M13.5 6.5l4 4"></path>
                      </svg>
                    </a>
                    <a href="#" class="list-group-item-actions">
                      <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-trash" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                        <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                        <path d="M4 7l16 0"></path>
                        <path d="M10 11l0 6"></path>
                        <path d="M14 11l0 6"></path>
                        <path d="M5 7l1 12a2 2 0 0 0 2 2h8a2 2 0 0 0 2 -2l1 -12"></path>
                        <path d="M9 7v-3a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v3"></path>
                      </svg>
                    </a>                    
                  </div>
                </div>
              </div>
             
            </div>
          </div>
        </div>        
      </div>
    </div>

  `,
  styles: [
  ]
})
export class DashboardComponent {
  
  activity_date: Date | undefined;
  consumableData: any[] = [];

  constructor(
    private http: HttpClient, 
    private authService: AuthService,
    private consumableService: ConsumableService
  ) {}

  ngOnInit() {
    this.activityDate();
  }

  activityDate() {

    const element = document.getElementById('datepicker');

    // Set the activity date to today if not set
    if (this.activity_date == undefined) {
      this.activity_date = new Date();

      // Get activity data based on selected date
      let start_date = new Date(this.activity_date!.getFullYear(), this.activity_date!.getMonth(), this.activity_date!.getDate(), 0, 0, 0, 0);
      let end_date = new Date(this.activity_date!.getFullYear(), this.activity_date!.getMonth(), this.activity_date!.getDate(), 23, 59, 59, 999);
      this.fetchConsumableData(start_date, end_date);

    }
    
    if (element) {
      const picker = new Litepicker({
        element: element,
        singleMode: true,
        tooltipText: { one: 'night', other: 'nights' },
        tooltipNumber: (totalDays) => totalDays - 1        
      });
  
      picker.on('selected', () => {
        const activity_date = picker.getDate();
        this.activity_date = activity_date?.toJSDate();

        // Get activity data based on selected date
        let start_date = new Date(this.activity_date!.getFullYear(), this.activity_date!.getMonth(), this.activity_date!.getDate(), 0, 0, 0, 0);
        let end_date = new Date(this.activity_date!.getFullYear(), this.activity_date!.getMonth(), this.activity_date!.getDate(), 23, 59, 59, 999);
        this.fetchConsumableData(start_date, end_date);

        picker.hide();
      });

    }

  }
  
  // Call API
  fetchConsumableData(start_date: Date, end_date: Date) {
    this.consumableService.fetchConsumableData(start_date, end_date).subscribe(
      (data) => {
        console.log(data);
        // Handle the response data here
        this.consumableData = data;
      },
      (error) => {
        console.error(error);
        // Handle the error here
      }
    );
  }  

}

