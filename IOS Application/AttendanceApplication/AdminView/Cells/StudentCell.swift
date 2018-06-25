//
//  StudentCell.swift
//  AttendanceApplication
//

import Foundation
import UIKit

class StudentCell: UITableViewCell {
    
    // MARK: IBOutlets
    
    @IBOutlet weak var studentName: UILabel!
    @IBOutlet weak var studentEmail: UILabel!
    
    // MARK: Public methods
    
    func setLabels(student: Student) {
        self.studentName.text = student.name
        self.studentEmail.text = student.email
    }
}
