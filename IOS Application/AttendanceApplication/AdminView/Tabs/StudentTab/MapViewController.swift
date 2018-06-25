//
//  MapViewController.swift
//  AttendanceApplication
//

import Foundation
import UIKit

class MapViewController: UIViewController {
    
    // MARK: IBOutlets
    
    @IBOutlet weak var modalView: UIView!
    @IBOutlet weak var roomNumber: UILabel!
    @IBOutlet weak var zoneName: UILabel!
    @IBOutlet weak var timestamp: UILabel!
    @IBOutlet weak var imageView: UIImageView!
    
    // MARK: Public properties
    
    var location: Location!
    
    // MARK: UIViewController methods
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        modalView.layer.cornerRadius = 10
        
        // Set the labels
        setLabels()
    }
    
    // MARK: IBAction methods
    
    @IBAction func dismissModal(_ sender: Any) {
        dismiss(animated: true, completion: nil)
    }
    
    // MARK: Internal methods
    
    internal func setLabels() {
        self.roomNumber.text = location.roomNumber
        self.zoneName.text = location.description
        self.timestamp.text = location.timestamp
        let fileName = "zone-" + location.zoneId
        imageView.image = UIImage(named: fileName)!
    }
}
