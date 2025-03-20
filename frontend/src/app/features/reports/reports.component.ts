import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/core/api.service';
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

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.fetchReports();
  }

  fetchReports(): void {
    this.apiService.getReports().subscribe((data) => {
      this.reportData = data;
    });
  }
}
