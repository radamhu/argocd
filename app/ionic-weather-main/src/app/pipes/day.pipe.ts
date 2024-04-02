import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'day'
})
export class DayPipe implements PipeTransform {

  transform(value: string): string {
    // mivel a value string-ként érkezik +value-val számmá alakítjuk
  let a = new Date(+value * 1000);
  let days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
  // create an array of days of week, getDay method reurn numbers,
  // we can use that number as an index of array, if get 0 = Sunday
  return days[a.getDay()]
  }
}
