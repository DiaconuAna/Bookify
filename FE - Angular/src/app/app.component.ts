import {Component, OnInit} from '@angular/core';
import {AuthService} from "./service/auth.service";
import {UserProfile} from "./model/user-profile";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit{
  constructor(private authService: AuthService) {}
  title = 'BookShazamFE';
  userProfile?: UserProfile | null;

  ngOnInit(): void {
    this.authService.userProfile.subscribe((data) => {
      this.userProfile = data;
    });
  }
}
