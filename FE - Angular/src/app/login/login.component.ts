import { Component, OnInit } from '@angular/core';
//import {User} from "../model/user";
import {Router} from "@angular/router";
import {LoginService} from "../service/login.service";
import {Login} from "../model/user_request";
import {AuthService} from "../service/auth.service";
import {TokenModel} from "../model/token-model";
import {BehaviorSubject} from "rxjs";
import {User} from "../model/user";
import {JwtHelperService} from "@auth0/angular-jwt";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {


  username!: string;
  password!: string;
  loginResponse!: string;
  userProfile = new BehaviorSubject<User | null>(null);
  jwtService: JwtHelperService = new JwtHelperService();

  constructor(private login: LoginService, private router: Router, private auth: AuthService) { }

  ngOnInit(): void {
    this.router.routeReuseStrategy.shouldReuseRoute = () => false;
  }

  clickLogin(username: string, password: string): void{
    this.login.loginRequest(<Login>{username:username, password:password}).subscribe(

      response => {
        var token = <TokenModel>{access_token: response.body.access, refresh_token: response.body.refresh}
        localStorage.setItem('tokens', JSON.stringify(token));
        console.log(username)
        localStorage.setItem('username', username)
        localStorage.setItem("jwt", response.body.user.access);
        localStorage.setItem("refresh", response.body.user.refresh);
        console.log(response)
        if(response.status == 200) {
          this.loginResponse = 'Login successful'
          this.router.navigate(['/main']);
        }
        else
          this.loginResponse = 'Login unsuccessful'
      },
      error =>{
        console.log(error)
        this.loginResponse = error.error.error
      }
      )}

}
