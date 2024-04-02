import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'dateFormatting'
})
export class DateFormattingPipe implements PipeTransform {

  transform(unixTimeStamp: string): unknown {
    let a = new Date(+unixTimeStamp * 1000);
    let months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    let days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    return days[a.getDay()] + ', ' + a.getDate() + ' ' + months[a.getMonth()] + ' ' + a.getHours() + ':' + a.getMinutes();
  }
}
