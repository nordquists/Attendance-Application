//
//  AdminSettingsViewController.swift
//  AttendanceApplication
//
//  Created by Sean Nordquist on 1/19/18.
//  Copyright © 2018 Sean Nordquist. All rights reserved.
//

import UIKit

class AdminSettingsTabViewController: UIViewController {

    // MARK: IBAction methods
    
    @IBAction func logoutButton(_ sender: Any) {
        // Perform logout
        performLogout()
    }
    
    // MARK: Internal methods
    
    internal func performLogout() {
        // Dismiss the admin view
        dismiss(animated: true, completion: nil)
        // No clean up to be done
    }
}
