import {Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {TopNavigationComponent} from "../top-navigation/top-navigation.component";
import {NgForm} from "@angular/forms";
import {MainService} from "../service/main.service";
import {Router} from "@angular/router";
import {fromEvent} from "rxjs";
import {userBook} from "../model/userBook";

@Component({
  selector: 'app-user-books',
  templateUrl: './user-books.component.html',
  styleUrls: ['./user-books.component.css']
})
export class UserBooksComponent implements OnInit {

  @ViewChild(TopNavigationComponent) topNav: TopNavigationComponent | undefined;
  @ViewChild('myForm') form: NgForm | undefined;
  @ViewChild('list') list: ElementRef | undefined;

  isLoading = true;
  hasInfo = false;

  userBooks!: userBook[];
  filteredBooks!: userBook[];
  pagedBooks!: userBook[];

  page = 1;
  pageSize = 5;

  readChecked = false;
  toReadChecked = false;
  currentlyReadingChecked = false;

  searchQuery = "";

  constructor(private bookService: MainService, private router: Router) {
    fromEvent(document, 'click').subscribe(() => {
      // @ts-ignore
      this.topNav?.showList = false;
    });
  }

  ngOnInit(): void {
    this.getUserBooks();
  }

  getUserBooks() {
    let username = ""
    if (localStorage.getItem('username') != null) { // @ts-ignore
      username = localStorage.getItem('username')
    }
    this.bookService.getUserBooks(username).subscribe(
      res => {
        this.isLoading = false;
        this.userBooks = res;
        if (res.length == 0) {
          this.hasInfo = false;
        } else {
          this.hasInfo = true;
          this.filteredBooks = this.userBooks;
          this.pagedBooks = this.filteredBooks.slice(0, this.pageSize);
        }
      },
      error => {
        console.log(error)
      }
    )
  }

  searchBook(book_id: string) {
    this.router.navigate(['/book', book_id])
  }

  refreshBooks() {
    // console.log("Page: " + this.page + " -- size: " + this.pageSize);
    // console.log((this.page-1)*this.pageSize, (this.page-1)*this.pageSize + this.pageSize);
    this.pagedBooks = this.filteredBooks.slice((this.page - 1) * this.pageSize, (this.page - 1) * this.pageSize + this.pageSize)
  }

  refreshBooksFilter(){
    console.log(this.searchQuery)
    this.filterByShelf();
    this.filteredBooks = this.filteredBooks.filter((book: userBook) => this.checkSearch(book));
    this.page = 1;
    this.refreshBooks();
  }

  filterByShelf() {
    if (!this.toReadChecked && !this.readChecked && !this.currentlyReadingChecked) {
      this.filteredBooks = this.userBooks;
    } else {
      this.filteredBooks = this.userBooks.filter(book => {
        if (this.readChecked && book.shelf === 'Read') {
          return true;
        }
        if (this.toReadChecked && book.shelf === 'To Read') {
          return true;
        }
        return this.currentlyReadingChecked && book.shelf === 'Currently Reading';

      });
    }
    // this.page = 1;
    // this.refreshBooks();
  }

  checkSearch(book: userBook){
    if(this.searchQuery == '') return true;
    let titleCondition = book.title.toLowerCase().includes(this.searchQuery?.toLowerCase() || '')
    let authorCondition = book.author.toLowerCase().includes(this.searchQuery?.toLowerCase() || '')
    let genreCondition = book.genre.toLowerCase().includes(this.searchQuery?.toLowerCase() || '')
    return titleCondition || authorCondition || genreCondition
  }

}
