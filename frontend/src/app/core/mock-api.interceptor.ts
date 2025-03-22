import { HttpInterceptorFn, HttpResponse } from '@angular/common/http';
import { of } from 'rxjs';

export const mockApiInterceptor: HttpInterceptorFn = (req, next) => {
  if (req.url.endsWith('/reports')) {
    return of(
      new HttpResponse({
        status: 200,
        body: [
          { id: 1, name: 'Q1 Report', value: 12500 },
          { id: 2, name: 'Q2 Report', value: 15000 },
        ],
      })
    );
  }

  if (req.url.endsWith('/transactions')) {
    return of(
      new HttpResponse({
        status: 200,
        body: [
          { id: 1, date: '2023-01-15', amount: 1200, type: 'income' },
          { id: 2, date: '2023-01-20', amount: 500, type: 'expense' },
        ],
      })
    );
  }

  return next(req);
};
