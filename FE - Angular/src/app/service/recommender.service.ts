import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Observable} from "rxjs";

const BOOK_API = 'http://127.0.0.1:5000/api/books'

@Injectable({
  providedIn: 'root'
})
export class RecommenderService{
  constructor(private httpClient: HttpClient) { }

  //todo : add authentication
  getRecommendationsModel1(text: String, criteria: String, top: number): Observable<any>{
    console.log(text)
    return this.httpClient.get("http://localhost:5000/api/books/descriptionRec?text=" + text + "&criteria=" + `${criteria}` + "&top=" + `${top}`)
  }

  getUserProfileRecommendations(username: string): Observable<any>{
    return this.httpClient.get("http://localhost:5000/api/books/profileRec?username="+`${username}`)
  }
}
