import {Component, ElementRef, ViewChild} from '@angular/core';
import {MainService} from "../service/main.service";
import {Router} from "@angular/router";
import {MatIconModule} from '@angular/material/icon';
import {faSearch} from '@fortawesome/free-solid-svg-icons';
import {bookTitle} from "../model/book_title";
import {fromEvent} from "rxjs";
import {TopNavigationComponent} from "../top-navigation/top-navigation.component";
import {searchBook} from "../model/search_book";

@Component({
  selector: 'app-main-page',
  templateUrl: './main-page.component.html',
  styleUrls: ['./main-page.component.css']
})
export class MainPageComponent {

  @ViewChild(TopNavigationComponent) topNav: TopNavigationComponent | undefined;

  readBooks!: searchBook[];
  toReadBooks!: searchBook[];
  currentlyReadingBooks!: searchBook[];

  isLoading = true;
  hasInfo = true;
  username = "";

  constructor(private bookService: MainService, private router: Router) {
    fromEvent(document, 'click').subscribe(() => {
      // @ts-ignore
      this.topNav?.showList = false;
    });

  }

  ngOnInit(): void {
  this.getMainPageBooks()
  }

  getMainPageBooks(){
    let username = ""
    if (localStorage.getItem('username') != null) { // @ts-ignore
      username = localStorage.getItem('username')
      this.username = username;
    }
    this.bookService.getMainPageBooks(username).subscribe(
      res => {
        console.log(res.books)
        this.readBooks = res.books.read;
        this.currentlyReadingBooks = res.books.currently_reading;
        this.toReadBooks = res.books.to_read;
        this.isLoading = false;
        if(res.books.read == 0 && res.books.currently_reading == 0 && res.books.to_read == 0){
          this.hasInfo = false;
        }
      },
      error => {
        console.log(error)
      }
    )
  }

  searchBook(book: string) {
    this.router.navigate(['/book', book])
  }


}
