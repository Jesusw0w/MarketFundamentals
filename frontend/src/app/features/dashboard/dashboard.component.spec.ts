import { ComponentFixture, TestBed } from '@angular/core/testing';
import { DashboardComponent } from './dashboard.component';
import { ApiService } from '../../core/api.service';
import { provideHttpClient } from '@angular/common/http';
import { of } from 'rxjs';
import { MatCardModule } from '@angular/material/card';
import { NavbarComponent } from '../../shared/navbar/navbar.component';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';

describe('DashboardComponent', () => {
  let component: DashboardComponent;
  let fixture: ComponentFixture<DashboardComponent>;
  let apiServiceMock: jasmine.SpyObj<ApiService>;

  beforeEach(async () => {
    apiServiceMock = jasmine.createSpyObj('ApiService', ['getTransactions']);
    apiServiceMock.getTransactions.and.returnValue(of([]));

    await TestBed.configureTestingModule({
      imports: [DashboardComponent, MatCardModule, NoopAnimationsModule],
      providers: [
        provideHttpClient(),
        { provide: ApiService, useValue: apiServiceMock },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(DashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
