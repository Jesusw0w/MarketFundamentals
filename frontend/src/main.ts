import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { provideRouter } from '@angular/router';
import { routes } from './app/app.routes';
import { importProvidersFrom } from '@angular/core';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { mockApiInterceptor } from './app/core/mock-api.interceptor';

bootstrapApplication(AppComponent, {
  providers: [
    provideHttpClient(withInterceptors([mockApiInterceptor])),
    provideRouter(routes),
    importProvidersFrom(BrowserAnimationsModule),
  ],
}).catch((err) => console.error('Error bootstrapping app:', err));
