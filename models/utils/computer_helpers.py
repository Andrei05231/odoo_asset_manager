
def _find_computer( Computer, serial_number, name):
     """
     Try to find a computer by serial number first, then by name.
     """
     search_fields = [
         ('serialNumber', serial_number, 'serialNumber'),
         ('name', name, 'name'),
     ]
     for field, value, match_type in search_fields:
         if value:
             record = Computer.search(
                 [(field, '=', value)],
                 limit=1
             )
             if record:
                 return record, match_type
     return None, None

def _extract_update_values( computer_data):
     """
     Extract only allowed fields for update.
     """
     updatable_fields = {
         'cpu',
         'gpu',
         'memory',
     }
     vals = {}
     for field, value in computer_data.items():
         if field in updatable_fields:
             vals[field] = value
     return vals

def _process_computer_update( Computer, computer_data, logger):
     """
     Update a single computer record.
     """
     serial_number = computer_data.get('serialNumber')
     name = computer_data.get('name')
     computer, match_field = _find_computer(
         Computer,
         serial_number,
         name
     )
     update_vals = _extract_update_values(computer_data)
     if not computer:
         try:
             Computer.create(update_vals)
             return {
             'serialNumber': serial_number,
             'name': name,
             'status': 'Created'
         }

         except Exception as e :
             logger.error(f"Can t create computer : {e}")
             return {
             'serialNumber': serial_number,
             'name': name,
             'status': 'not_found'
         }
         
     
     if not update_vals:
         return {
             'serialNumber': serial_number,
             'name': name,
             'status': 'no_updates',
             'id': computer.id
         }
     try:
         computer.write(update_vals)
         return {
             'serialNumber': serial_number,
             'name': name,
             'status': 'updated',
             'id': computer.id,
             'matched_by': match_field
         }
     except Exception as e:
         logger.exception(
             "Error updating computer %s",
             serial_number or name
         )
         return {
             'serialNumber': serial_number,
             'name': name,
             'status': 'error',
             'error': str(e)
         }
     
def _calculate_summary( results):
     """
     Summarize batch results.
     """
     status_counts = {}
     for result in results:
         status = result.get('status')
         if status:
             status_counts[status] = status_counts.get(status, 0) + 1
     return {
         'total': len(results),
         'updated': status_counts.get('updated', 0),
         'not_found': status_counts.get('not_found', 0),
         'errors': status_counts.get('error', 0),
     }