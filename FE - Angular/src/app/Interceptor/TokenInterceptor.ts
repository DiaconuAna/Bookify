import {Injectable} from '@angular/core';
import {HttpEvent, HttpHandler, HttpHeaders, HttpInterceptor, HttpRequest} from '@angular/common/http';
import {catchError, Observable, switchMap, throwError} from 'rxjs';
import {AuthService} from "../service/auth.service";
import { JwtHelperService } from '@auth0/angular-jwt';


@Injectable()
export class TokenInterceptor implements HttpInterceptor {

  urlsToNotUse: Array<string>;
  refreshUrl: string;

  constructor(private auth: AuthService, private jwtHelper: JwtHelperService) {
    this.urlsToNotUse = [
      'http://127.0.0.1:5000/api/auth/login',
      'localhost:5000/api/auth/login',
      'localhost:5000/api/auth/register',
    ];
    this.refreshUrl = 'http://127.0.0.1:5000/api/auth/token/refresh'
  }

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    var token = localStorage.getItem("jwt")
    var refresh_token = localStorage.getItem("refresh")
    if(request.url == this.refreshUrl){
      let interceptedRequest = request.clone({
        setHeaders: {
          Authorization: `Bearer ${refresh_token}`
        }
      });
      return next.handle(interceptedRequest);
    }
    if (token) {
      if (this.jwtHelper.isTokenExpired(token)) {
        console.log("expired");
      } else {
        console.log("valid");
      }
      var tokenExpirationDate = this.jwtHelper.getTokenExpirationDate(token)
      var currentDate = new Date()
      console.log("1." + tokenExpirationDate + "\n2. " + currentDate)
      // @ts-ignore
      if (tokenExpirationDate < currentDate) {
        // send request to refresh token
        return this.auth.getRefreshToken().pipe(
          switchMap((response: any) => {
            console.log("hello")
            localStorage.setItem('jwt', response.access);
            console.log(response.access)
            const newRequest = request.clone({
              setHeaders: {
                Authorization: `Bearer ${response.access}`
              }
            });
            return next.handle(newRequest);
          }),
          catchError(refreshError => {
            // Handle the case where the refresh token request fails
            return throwError(refreshError);
          })
        );

      } else {
        if (!this.urlsToNotUse.includes(request.url)) {
          let interceptedRequest = request.clone({
            setHeaders: {
              Authorization: `Bearer ${token}`
            }
          });
          return next.handle(interceptedRequest);
        }
      }
    }
    return next.handle(request);
  }
}
