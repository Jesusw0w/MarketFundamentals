import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../core/api.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-reports',
  templateUrl: './reports.component.html',
  styleUrls: ['./reports.component.css'],
  standalone: true,
  imports: [CommonModule],
})
export class ReportsComponent implements OnInit {
  reportData: any;
  loading = false;
  error: string | null = null;

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.fetchReports();
  }

  fetchReports(): void {
    this.loading = true;
    this.error = null;

    this.apiService.getReports().subscribe({
      next: (data: any) => {
        this.reportData = data;
        this.loading = false;
        console.log('Reports data:', data);
      },
      error: (error: any) => {
        this.error = 'Failed to load reports';
        this.loading = false;
        console.error('Error fetching reports:', error);
      },
    });
  }
}
