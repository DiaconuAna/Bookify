import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import { JwtHelperService } from '@auth0/angular-jwt';
import {BehaviorSubject, catchError, map, Observable, of} from 'rxjs';
import {User} from "../model/user";
import {Login} from "../model/user_request";
import {TokenModel} from "../model/token-model";
import {UserData} from "../model/userdata";
import {UserProfile} from "../model/user-profile";

const AUTH_API = 'http://127.0.0.1:5000/api/auth'

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(private httpClient: HttpClient) {}
  userProfile = new BehaviorSubject<UserProfile | null>(null);
  jwtService: JwtHelperService = new JwtHelperService();

  userLogin(payload: Login){
    return this.httpClient.post<any>(AUTH_API+"/login", payload, {observe: "response"}).pipe(
      map(
        (response) =>{
          console.log("User data:" + response)
          return true;
        }
      ),
      catchError((error) => {
        console.log(error);
        return of(false);
      })
    )
  }

  getAccessToken(): string{
    var localStorageToken = localStorage.getItem('tokens');
    if(localStorageToken){
      var token = JSON.parse(localStorageToken) as TokenModel;
      var isTokenExpired = this.jwtService.isTokenExpired(token.access_token);
      if(isTokenExpired){
        this.userProfile.next(null);
        return "";
      }
      var userInfo = this.jwtService.decodeToken(
        token.access_token
      ) as UserProfile;
      this.userProfile.next(userInfo);
      return token.access_token;
    }
    return "";
  }

  getRefreshToken(): Observable<any>{
    console.log("tw3")
    // const refreshToken = localStorage.getItem('refresh');
    // // const jwtToken = localStorage.getItem('jwt_token');
    //
    // const headers: HttpHeaders  = new HttpHeaders()
    //   .set('Authorization', 'Bearer ' + refreshToken)
    //   .set('Content-Type', 'application/json');

    // const headers = {
    //   Authorization: `Bearer ${refreshToken}`
    // };
    // console.log(headers)
    return this.httpClient.get<any>(AUTH_API+"/token/refresh", );
  }
}
