import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {Login} from "../model/user_request";
import {Register} from "../model/register-request";

const AUTH_API = 'http://127.0.0.1:5000/api/auth'

@Injectable({
  providedIn: 'root'
})
export class RegisterService {


  constructor(private httpClient: HttpClient) { }

  registerRequest(register_request: Register): Observable<any> {
    return this.httpClient.post<any>(AUTH_API+"/register", register_request, {observe: "response"});
  }

}
