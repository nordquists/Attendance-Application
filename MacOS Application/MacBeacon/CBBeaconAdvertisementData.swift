//
// --- This is NOT my code, it is an edited version of the code (to fit my use) created by Mathew Robinson.
//
//  CBBeaconAvertisementData.swift
//  iBeaconSwiftOSX
//
//  Created by Marcelo Gigirey on 11/5/14.
//  Copyright (c) 2014 Marcelo Gigirey. All rights reserved.
//
//  Licensed under the Apache License, Version 2.0 (the "License");
//  you may not use this file except in compliance with the License.
//  You may obtain a copy of the License at
//
//  http://www.apache.org/licenses/LICENSE-2.0
//
//  Unless required by applicable law or agreed to in writing, software
//  distributed under the License is distributed on an "AS IS" BASIS,
//  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//  See the License for the specific language governing permissions and
//  limitations under the License.
//
//  Portions of this code are from BLCBeaconAdvertisement.m, part of BeaconOSX under this license:
//
//  Copyright (c) 2013, Matthew Robinson
//  All rights reserved.
//
//  Redistribution and use in source and binary forms, with or without modification,
//  are permitted provided that the following conditions are met:
//
//  1. Redistributions of source code must retain the above copyright notice, this
//  list of conditions and the following disclaimer.
//
//  2. Redistributions in binary form must reproduce the above copyright notice,
//  this list of conditions and the following disclaimer in the documentation
//  and/or other materials provided with the distribution.
//
//  3. Neither the name of Blended Cocoa nor the names of its contributors may
//  be used to endorse or promote products derived from this software without
//  specific prior written permission.
//
//  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
//  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
//  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
//  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
//  INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
//  NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
//  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
//  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
//  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
//  POSSIBILITY OF SUCH DAMAGE.
//
// --- This is NOT my code, it is an edited version of the code (to fit my use) created by Mathew Robinson.


import Foundation
import CoreBluetooth
import CoreLocation
    
final class CBBeaconAvertisementData: NSObject {
    
    // MARK: Public properties
    
    var proximityUUID: NSUUID
    var major:  CLBeaconMajorValue
    var minor: CLBeaconMinorValue
    var measuredPower: Int8
    
    // MARK: Init
        
    init(proximityUUID: NSUUID?, major: CLBeaconMajorValue?, minor: CLBeaconMinorValue?, measuredPower: Int8?) {
        self.proximityUUID = proximityUUID!
        self.major = major!
        self.minor = minor!
        self.measuredPower = measuredPower!
    }
    
    // MARK: Public methods
    
    func beaconAdvertisement() -> NSDictionary? {
        let bufferSize = 21
        let beaconPreamble: NSString = "kCBAdvDataAppleBeaconKey";
        
        var advertisementBytes = [CUnsignedChar](repeating: 0, count: bufferSize)

        proximityUUID.getBytes(&advertisementBytes)
    
        advertisementBytes[16] = CUnsignedChar(major >> 8)
        advertisementBytes[17] = CUnsignedChar(major & 255)
        
        advertisementBytes[18] = CUnsignedChar(minor >> 8)
        advertisementBytes[19] = CUnsignedChar(minor & 255)
        
        advertisementBytes[20] = CUnsignedChar(bitPattern: measuredPower)
        
        let advertisement = NSData(bytes: advertisementBytes, length: bufferSize)
        
        return NSDictionary(object: advertisement, forKey: beaconPreamble)
    }
}
