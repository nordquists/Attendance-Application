//
//  LocationCell.swift
//  AttendanceApplication
//

import Foundation
import UIKit

class LocationCell: UITableViewCell {
    
    // MARK: IBOutlets
    
    @IBOutlet weak var roomNumber: UILabel!
    @IBOutlet weak var desc: UILabel!
    @IBOutlet weak var timestamp: UILabel!
    
    // MARK: Public methods
    
    func setLabels(location: Location) {
        self.roomNumber.text = location.roomNumber
        self.desc.text = location.description
        
        // Time stamp must be formated before being displayed to prevent clipping.
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "yyyy-MM-dd HH:mm:ss.SSSSSS"
        let date = dateFormatter.date(from: location.timestamp)
        let calendar = NSCalendar.current
        
        // Set the format of the date depending on the timestamp's day. This is for readability purposes, and extensibility.
        if calendar.isDateInToday(date!) {
            dateFormatter.dateFormat = "HH:mm"
        } else {
            dateFormatter.dateFormat = "dd-MM-YY HH:mm:ss"
        }
        
        // Finish by converting the date into a string and giving the label the value.
        self.timestamp.text = dateFormatter.string(from: date!)
    }
}

