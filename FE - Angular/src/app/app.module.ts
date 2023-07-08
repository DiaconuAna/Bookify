import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import {HTTP_INTERCEPTORS, HttpClientModule} from "@angular/common/http";
import {RouterModule} from "@angular/router";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import { JwtModule, JWT_OPTIONS } from '@auth0/angular-jwt';

import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { MainPageComponent } from './main-page/main-page.component';
import {AuthService} from "./service/auth.service";
import {AuthGuard} from "./guards/auth-guard.service";
import {TokenInterceptor} from "./Interceptor/TokenInterceptor";
import { RegisterComponent } from './register/register.component';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import {MatMenuModule} from "@angular/material/menu";
import {MatIconModule} from "@angular/material/icon";
import {MatButtonModule} from "@angular/material/button";
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import {MatFormFieldModule} from "@angular/material/form-field";
import { SearchPageComponent } from './search-page/search-page.component';
import {MatListModule} from "@angular/material/list";
import { BookPageComponent } from './book-page/book-page.component';
import { DescriptionRecommendationComponent } from './description-recommendation/description-recommendation.component';
import {MatProgressSpinnerModule} from "@angular/material/progress-spinner";
import { ModalShelfConfirmationComponent } from './modal-shelf-confirmation/modal-shelf-confirmation.component';
import { BookReviewPageComponent } from './book-review-page/book-review-page.component';
import { AuthorPageComponent } from './author-page/author-page.component';
import { TopNavigationComponent } from './top-navigation/top-navigation.component';
import { ModalUserReviewComponent } from './modal-user-review/modal-user-review.component';
import { UserProfileRecommendationComponent } from './user-profile-recommendation/user-profile-recommendation.component';
import { UserBooksComponent } from './user-books/user-books.component';
export function jwtOptionFactor(authService:AuthService){
  return {
    tokenGetter:() => {
      var accesstoken =  authService.getAccessToken();
      console.log(accesstoken)
      return accesstoken
    },
    allowedDomains:['127.0.0.1:5000'],
    disallowedRoutes:[
      "localhost:5000/api/auth/login"
    ]
  }
}

export function tokenGetter() {
  console.log("Local jwt: " + localStorage.getItem("jwt"))
  return localStorage.getItem("jwt");
}


@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    MainPageComponent,
    RegisterComponent,
    SearchPageComponent,
    BookPageComponent,
    DescriptionRecommendationComponent,
    ModalShelfConfirmationComponent,
    BookReviewPageComponent,
    AuthorPageComponent,
    TopNavigationComponent,
    ModalUserReviewComponent,
    UserProfileRecommendationComponent,
    UserBooksComponent,
  ],
  imports: [
    ReactiveFormsModule,
    BrowserModule,
    FormsModule,
    RouterModule.forRoot([
      {path: "", component: LoginComponent},
      {path: "register", component: RegisterComponent},
      {path: "main", component: MainPageComponent, canActivate: [AuthGuard]},
      {path: "search", component: SearchPageComponent, canActivate: [AuthGuard]},
      {path: "descriptionRec", component: DescriptionRecommendationComponent, canActivate: [AuthGuard]},
      {path: "profileRec", component: UserProfileRecommendationComponent, canActivate: [AuthGuard]},
      {path: "userBooks", component: UserBooksComponent, canActivate: [AuthGuard]},
      {path: "book/:title", component: BookPageComponent, canActivate: [AuthGuard]},
      {path: "review/:title", component: BookReviewPageComponent, canActivate: [AuthGuard]},
      {path: "author/:name", component: AuthorPageComponent, canActivate: [AuthGuard]}
    ]),
    JwtModule.forRoot({
      config: {
        tokenGetter: tokenGetter,
        allowedDomains: ['localhost:5000'],
        disallowedRoutes: ['localhost:5000/api/auth/login'],
      }
    }),
    HttpClientModule,
    FontAwesomeModule,
    MatMenuModule,
    MatIconModule,
    MatButtonModule,
    NgbModule,
    MatFormFieldModule,
    MatListModule,
    MatProgressSpinnerModule,
    MatProgressSpinnerModule
  ],
  providers: [AuthGuard,
    {
      provide: HTTP_INTERCEPTORS,
      useClass: TokenInterceptor,
      multi: true
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
