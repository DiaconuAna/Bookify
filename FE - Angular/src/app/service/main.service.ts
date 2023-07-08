import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Observable} from "rxjs";
import {RatingDTO} from "../model/rating_dto";

const BOOK_API = 'http://127.0.0.1:5000/api/books'

@Injectable({
  providedIn: 'root'
})
export class MainService {
  constructor(private httpClient: HttpClient) {
  }

  getPreliminaryBooks(): Observable<any> {
    console.log("token:: " + localStorage.getItem("jwt"))
    var token = localStorage.getItem("jwt")
    let headers = new HttpHeaders();
    headers.append('Content-Type', 'application/json');
    headers.set('Authorization', `Bearer ${token}`);

    return this.httpClient.get(BOOK_API + '/all');
  }

  //todo : add authentication
  searchByTitle(title: String): Observable<any> {
    console.log("hello > >")
    title = title.replace('#', '%23')
    console.log(title)
    return this.httpClient.get("http://localhost:5000/api/books/search_books?title=" + `${title}`)
  }

  findBookByTitle(title: string): Observable<any> {
    // console.log(title)
    title = title.replaceAll('#', '%23')
    title = title.replaceAll('&', '%26')
    title = title.replaceAll('+', '%2B')
    // console.log(title)
    return this.httpClient.get("http://localhost:5000/api/books/get_book?title=" + `${title}`)
  }

  addBookToShelf(username: string, book_id: number, shelf_name: string) {
    let post_url = "http://localhost:5000/api/shelf/shelf_book"
    return this.httpClient.post<any>(post_url, {book_id: book_id, username:username, shelf_name:shelf_name});
  }

  getBookReviews(title: String): Observable<any>{
    title = title.replaceAll('#', '%23')
    title = title.replaceAll('&', '%26')
    title = title.replaceAll('+', '%2B')
    console.log(title)
    return this.httpClient.get("http://localhost:5000/api/books/get_reviews?title=" + `${title}`)
  }

  getBookByAuthor(author: string): Observable<any>{
    author = author.replaceAll('#', '%23')
    author = author.replaceAll('&', '%26')
    author = author.replaceAll('+', '%2B')
    return this.httpClient.get("http://localhost:5000/api/books/get_author?author=" + `${author}`)
  }

  addReview(rating: RatingDTO){
    let post_url =  "http://localhost:5000/api/books/add_rating"
    console.log(rating)
    return this.httpClient.post<any>(post_url, rating);
  }

  getUserReviews(username: string, title: string): Observable<any>{
    title = title.replaceAll('#', '%23')
    title = title.replaceAll('&', '%26')
    title = title.replaceAll('+', '%2B')
    return this.httpClient.get("http://localhost:5000/api/books/user_reviews_book?username=" + `${username}` + "&title=" + `${title}`)
  }

  getBookSentiments(title:  string): Observable<any>{
    title = title.replaceAll('#', '%23')
    title = title.replaceAll('&', '%26')
    title = title.replaceAll('+', '%2B')
    title = title.replaceAll('\'', '')
    return this.httpClient.get("http://localhost:5000/api/books/sentiments?title=" + `${title}`)
  }

  getReviewPolarity(id: number): Observable<any>{
    return this.httpClient.get("http://localhost:5000/api/books/rating_polarity?id=" + `${id}`)
  }

  getUserBooks(username: string): Observable<any>{
    return this.httpClient.get("http://localhost:5000/api/shelf/all_books?username=" + `${username}`)
  }

  getMainPageBooks(username: string): Observable<any>{
    return this.httpClient.get("http://localhost:5000/api/shelf/main_page?username=" + `${username}`)
  }
}
