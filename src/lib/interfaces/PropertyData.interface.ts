export interface PropertyData {
  id: string;
  name?: string;
  address_1?: string;
  address_2?: string;
  neighborhood?: string;
  city?: string;
  state?: string;
  zip_code?: string;
  country?: string;
  latitude?: number;
  longitude?: number;
  square_footage?: string;
}

export interface PropertyTableRowData {
  Name: string;
  City: string;
  State: string;
  Country: string;
  'Available Area': string;
}

export const TABLE_HEADERS = ['Name', 'City', 'State', 'Country', 'Available Area'];
