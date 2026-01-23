
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

def _extract_update_values( computer_data, creating):
     """
     Extract only allowed fields for update.
     """
     if not creating:
        updatable_fields = {
            'cpu',
            'gpu',
            'memory',
            'name'
        }
     else:
        updatable_fields = {
            'serialNumber',
            'name',
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
     
     if not computer:
         try:
             update_vals = _extract_update_values(computer_data, True)
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
    
     update_vals = _extract_update_values(computer_data, False)
     
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

def _process_monitor_data(Monitor, Computer, computer_data, logger):
    monitors_data = computer_data.get('monitors') or []
    monitors_found = 0
    monitors_created = 0
    monitors_relinked = 0

    if not monitors_data:
        logger.info(
            "No monitor data found for computer %s",
            computer_data.get('serial_number') or computer_data.get('name')
        )
        return {'status': 'No monitor data found'}

    computer, match_field = _find_computer(
        Computer,
        computer_data.get('serial_number'),
        computer_data.get('name'),
    )

    if not computer:
        logger.warning(
            "Cannot link monitors: computer not found (serial=%s, name=%s)",
            computer_data.get('serial_number'),
            computer_data.get('name'),
        )
        return {'status': 'Linked computer not found'}

    logger.debug(
        "Processing %s monitors for computer ID %s",
        len(monitors_data),
        computer.id
    )

    for monitor in monitors_data:
        serial = monitor.get('serial')

        if not serial:
            logger.warning(
                "Skipping monitor with missing serial for computer ID %s",
                computer.id
            )
            continue

        try:
            existing_monitor = Monitor.search(
                [('serial_number', '=', serial)],
                limit=1
            )

            if existing_monitor:
                if existing_monitor.computer_id.id != computer.id:
                    old_computer = existing_monitor.computer_id.id
                    existing_monitor.write({
                        'computer_id': computer.id
                    })
                    monitors_relinked += 1

                    logger.info(
                        "Relinked monitor %s from computer %s → %s",
                        serial,
                        old_computer,
                        computer.id
                    )
                else:
                    monitors_found += 1
                    logger.debug(
                        "Monitor %s already linked to computer %s",
                        serial,
                        computer.id
                    )
                continue

            Monitor.create({
                'name': monitor.get('name'),
                'serial_number': serial,
                'computer_id': computer.id,
            })
            monitors_created += 1

            logger.info(
                "Created new monitor %s linked to computer %s",
                serial,
                computer.id
            )

        except Exception:
            logger.exception(
                "Error processing monitor %s for computer %s",
                serial,
                computer.id
            )

    logger.info(
        "Monitor sync completed for computer %s "
        "(found=%s, relinked=%s, created=%s)",
        computer.id,
        monitors_found,
        monitors_relinked,
        monitors_created
    )

    return {
        'status': 'completed',
        'already_linked': monitors_found,
        'relinked': monitors_relinked,
        'created': monitors_created,
    }

