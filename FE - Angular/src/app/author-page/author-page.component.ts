import {Component, OnInit, ViewChild} from '@angular/core';
import {faSearch} from "@fortawesome/free-solid-svg-icons";
import {bookTitle} from "../model/book_title";
import {searchBook} from "../model/search_book";
import {Book} from "../model/book";
import {MainService} from "../service/main.service";
import {ActivatedRoute, Router} from "@angular/router";
import {TopNavigationComponent} from "../top-navigation/top-navigation.component";
import {fromEvent} from "rxjs";

@Component({
  selector: 'app-author-page',
  templateUrl: './author-page.component.html',
  styleUrls: ['./author-page.component.css']
})
export class AuthorPageComponent implements OnInit {

  @ViewChild(TopNavigationComponent) topNav: TopNavigationComponent | undefined;

  allBooks!: searchBook[];
  page = 1;
  isLoading = false;
  showList = false;
  authorBooks!: Book[];
  pagedAuthorBooks!: Book[];
  authorName!: string;

  pageCount = 0;

  constructor(private bookService: MainService, private router: Router, private route: ActivatedRoute) {
    route.params.subscribe(val =>{
      this.isLoading = true
      this.authorBooks = []
      this.authorName = this.route.snapshot.params['name']
      this.bookService.getBookByAuthor(this.authorName).subscribe(
        res =>{
          this.authorBooks = res
          this.isLoading = false
          this.pageCount = Math.floor(res.length / 10);
          if(res.length % 10){
            this.pageCount ++;
          }
        },
        error =>{
          console.log(error)
        }
      )
    })

    fromEvent(document, 'click').subscribe(() => {
      // @ts-ignore
      this.topNav?.showList = false;
    });
  }

  ngOnInit(): void {
  }

  searchBook(book: string) {
    this.router.navigate(['/book', book])
  }

  getPageInfo(){
    if(this.pageCount == this.page){
      console.log(this.authorBooks.length % 10);
      this.pagedAuthorBooks = this.authorBooks.slice(-(this.authorBooks.length%10))
    }
    else{
      let startIndex = (this.page - 1)*10
      let endIndex = (this.page * 10);
      this.pagedAuthorBooks = this.authorBooks.slice(startIndex, endIndex)
    }
  }

}
