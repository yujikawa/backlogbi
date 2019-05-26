import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';

import {MatToolbarModule} from '@angular/material/toolbar';
import {MatTableModule} from '@angular/material/table';
import {MatPaginatorModule} from '@angular/material/paginator';
import {MatSelectModule} from '@angular/material/select';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { DashboardComponent } from './pages/dashboard/dashboard.component';

import { ApiService } from './services/api.service';
import { ChartComponent } from './components/chart/chart.component';
import { FormsModule } from '@angular/forms';
import { MatButtonModule, MatInputModule, MatProgressSpinnerModule } from '@angular/material';

@NgModule({
  declarations: [
    AppComponent,
    DashboardComponent,
    ChartComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatToolbarModule,
    MatTableModule,
    MatPaginatorModule,
    HttpClientModule,
    MatSelectModule,
    FormsModule,
    MatButtonModule,
    MatInputModule,
    MatProgressSpinnerModule,
  ],
  providers: [ApiService],
  bootstrap: [AppComponent],
  exports: [
    ChartComponent
  ]
})
export class AppModule { }
