import { Component } from '@angular/core';
import { WeatherService  } from '../services/weather.service';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage {

  public res;

  constructor(private weatherAPI: WeatherService) { }

  ngOnInit() {
    this.getWeatherData();
  }

  getWeatherData() {
    this.weatherAPI.getWeatherData().subscribe((response) => {
      this.res = response;
      console.log(this.res);
    });
  }

  doRefresh(event) {
    console.log('Ion-refresh running ... ');
    this.weatherAPI.getWeatherData().subscribe((response) => {
      this.res = response;
      console.log(this.res);
      console.log('done reloading wether data. ');
      event.target.complete();
    });
  }
}
