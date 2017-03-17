//
//  AdpressoInterstitialAd.h
//  AdLantis iOS SDK
//
//  Copyright 2014 Atlantis. All rights reserved.
//
//

#import <Foundation/Foundation.h>

@protocol AdlantisInterstitialAdDelegate;
@class AdpressoTargetingParameters;

@interface AdpressoInterstitialAd : NSObject

+ (instancetype)interstitialAdWithPublisherId:(NSString*)publisherId;

- (void)show;

- (void)cancel;

@property (nonatomic,weak) id<AdlantisInterstitialAdDelegate> delegate;

@property (nonatomic,strong) AdpressoTargetingParameters *targetingParameters;

@end


@protocol AdlantisInterstitialAdDelegate <NSObject>

@optional

- (void)interstitialAdRequestComplete:(AdpressoInterstitialAd*)interstitialAd;

- (void)interstitialAdRequestFailed:(AdpressoInterstitialAd*)interstitialAd;

- (void)interstitialAdWillBePresented:(AdpressoInterstitialAd*)interstitialAd;

- (void)interstitialAdWasDismissed:(AdpressoInterstitialAd*)interstitialAd;

@end
