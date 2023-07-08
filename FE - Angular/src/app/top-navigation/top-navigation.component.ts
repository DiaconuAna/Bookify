import {Component, OnInit} from '@angular/core';
import {faSearch} from "@fortawesome/free-solid-svg-icons";
import {bookTitle} from "../model/book_title";
import {MainService} from "../service/main.service";
import {Router} from "@angular/router";
import {fromEvent} from "rxjs";

@Component({
  selector: 'app-top-navigation',
  templateUrl: './top-navigation.component.html',
  styleUrls: ['./top-navigation.component.css']
})
export class TopNavigationComponent implements OnInit {

  searchIcon = faSearch;
  title!: string;
  searchedBookTitles!: bookTitle[];
  showList = false;

  constructor(private bookService: MainService, private router: Router) {
    fromEvent(document, 'click').subscribe(event => {
      // @ts-ignore
      if (this.showList && !this.list.nativeElement.contains(event.target)) {
        this.showList = false;
      }
    });
  }

  ngOnInit(): void {
  }

  searchByTitle(title: string) {
    this.showList = true;
    console.log('>>>' + title)
    if (title == "")
      this.searchedBookTitles = []
    else {
      this.bookService.searchByTitle(title).subscribe(
        res => {
          console.log(res['titles'])
          this.searchedBookTitles = res['titles']
          // console.log(this.searchedBookTitles)
        },
        error => console.log(error)
      )
    }
  }

  searchDetailed() {
    this.router.navigate(['/search'])
  }

  searchBook(book: string) {
    this.router.navigate(['/book', book])
  }

  recommendDescription() {
    this.router.navigate(['/descriptionRec'])
  }

  recommendProfile() {
    this.router.navigate(['/profileRec'])
  }

}
