import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../core/api.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css'],
  standalone: true,
  imports: [CommonModule],
})
export class DashboardComponent implements OnInit {
  stats = [
    { label: 'Total Revenue', value: '$10,000' },
    { label: 'Total Expenses', value: '$4,500' },
  ];

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.apiService.getTransactions().subscribe((data: any) => {
      console.log('Transactions:', data);
    });
  }
}
