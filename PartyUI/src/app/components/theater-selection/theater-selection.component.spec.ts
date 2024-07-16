import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TheaterSelectionComponent } from './theater-selection.component';

describe('TheaterSelectionComponent', () => {
  let component: TheaterSelectionComponent;
  let fixture: ComponentFixture<TheaterSelectionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TheaterSelectionComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TheaterSelectionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
