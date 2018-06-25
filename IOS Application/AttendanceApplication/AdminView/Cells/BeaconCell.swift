//
//  BeaconCell.swift
//  AttendanceApplication
//

import Foundation
import UIKit

class BeaconCell: UITableViewCell {
    
    // MARK: IBOutlets
    
    @IBOutlet weak var roomNumber: UILabel!
    @IBOutlet weak var desc: UILabel!
    
    // MARK: Public methods
    
    func setLabels(beacon: Beacon){
        self.roomNumber.text = beacon.roomNumber
        self.desc.text = beacon.description
    }
}
