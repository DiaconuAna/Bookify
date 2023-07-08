import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {Login} from "../model/user_request";

const AUTH_API = 'http://127.0.0.1:5000/api/auth'

@Injectable({
  providedIn: 'root'
})
export class LoginService {


  constructor(private httpClient: HttpClient) { }


  loginRequest(user: Login): Observable<any> {
    return this.httpClient.post<any>(AUTH_API+"/login", user, {observe: "response"});
  }

}
