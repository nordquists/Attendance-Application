//
//  Beacon.swift
//  MacBeacon
//


import Foundation

class Beacon {
    
    // MARK: Public properties
    
    var roomNumber: String!
    var description: String!
    var id: String!
    var zoneName: String!
    var major: String!
    var minor: String!
    
    // MARK: Init
    
    init(beaconJSONObject: [String: String]) {
        if let roomNumber = beaconJSONObject["room_number"], let description = beaconJSONObject["description"], let id = beaconJSONObject["id"], let zoneName = beaconJSONObject["zone_name"], let major = beaconJSONObject["major"], let minor = beaconJSONObject["minor"]  {
            self.roomNumber = roomNumber
            self.description = description
            self.id = id
            self.zoneName = zoneName
            self.major = major
            self.minor = minor
        } else {
            self.roomNumber = "roomNumber"
            self.description = "description"
            self.id = "id"
            self.zoneName = "zoneName"
            self.major = "major"
            self.minor = "minor"
        }
    }
}
