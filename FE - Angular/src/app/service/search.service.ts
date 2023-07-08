import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Observable} from "rxjs";

const BOOK_API = 'http://127.0.0.1:5000/api/books'

@Injectable({
  providedIn: 'root'
})
export class SearchService {
  constructor(private httpClient: HttpClient) {
  }

  searchByTitle(title: String, page: number, size: number): Observable<any> {
    return this.httpClient.get("http://localhost:5000/api/books/search_detailed?criteria=title&page=" + `${page}` + "&size=" + `${size}` + "&title=" + `${title}`)
  }

  searchByAuthor(author: String, page: number, size: number): Observable<any> {
    return this.httpClient.get("http://localhost:5000/api/books/search_detailed?criteria=author&page=" + `${page}` + "&size=" + `${size}` + "&author=" + `${author}`)
  }

  searchByGenre(genre: String, page: number, size: number): Observable<any> {
    return this.httpClient.get("http://localhost:5000/api/books/search_detailed?criteria=genre&page=" + `${page}` + "&size=" + `${size}` + "&genre=" + `${genre}`)
  }

}
