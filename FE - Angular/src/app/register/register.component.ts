import {Component, OnInit} from '@angular/core';
import {Router} from "@angular/router";
import {AbstractControl, FormControl, FormGroup, ValidatorFn, Validators} from "@angular/forms";
import {LoginService} from "../service/login.service";
import {RegisterService} from "../service/register.service";
import {Register} from "../model/register-request";


@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {

  bookForm!: FormGroup;
  registerResponse!: string;

  user = {username: "", email: "", password: "", cb: false}

  constructor(private registerService: RegisterService, private router: Router) {
  }

  get username() {
    return this.bookForm.get("username")!;
  }

  get email() {
    return this.bookForm.get("email")!;
  }

  get password() {
    return this.bookForm.get("password")!;
  }

  // username, email, password

  ngOnInit(): void {
    this.registerResponse = "";
    // @ts-ignore
    this.bookForm = new FormGroup(
      {
        username: new FormControl(this.user.username,
          [
            Validators.required,
            Validators.minLength(4)
            // add validator for alpha
          ]),
        email: new FormControl(this.user.email,
          [
            Validators.required,
            Validators.email,
          ]),
        password: new FormControl(this.user.password,
          [
            Validators.required,
            Validators.minLength(6)
          ]),
        cb: new FormControl(this.user.cb,
          [ Validators.requiredTrue]
        )

      }
    )
  }

  register() {
    console.log(this.username.value, " ", this.password.value)
    this.registerService.registerRequest(<Register>{
      username: this.username.value,
      password: this.password.value,
      email: this.email.value
    }).subscribe(
      response => {
        console.log(response.status)
        if (response.status == 201) {
          this.router.navigate([''])
        } else {
          console.log("Register unsuccessful")
          console.log("response")
        }
      },
      error => {
        console.log("Register unsuccessful")
        this.registerResponse = error.error.error
      }
    )
  }

}
