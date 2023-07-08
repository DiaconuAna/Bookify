import { Component, OnInit } from '@angular/core';
import {NgbActiveModal, NgbRating} from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-modal-user-review',
  templateUrl: './modal-user-review.component.html',
  styleUrls: ['./modal-user-review.component.css']
})
export class ModalUserReviewComponent implements OnInit {

  currentRate = 0;
  floatRate = 3.14;
  invalidRating = false;

  reviewText = ""
  reviewSummary = ""
  someInput: string | undefined;

  constructor(public activeModal: NgbActiveModal) {}

  close() {
    console.log(this.floatRate)
    if(!this.currentRate){
      this.invalidRating= true;
      return;
    }
    const result = {
      rating: this.currentRate,
      summary: this.reviewSummary,
      text: this.reviewText
    }
    this.activeModal.close(result);
  }

  dismiss(reason: string) {
    this.activeModal.dismiss(reason);
  }

  ngOnInit(): void {
  }


}
