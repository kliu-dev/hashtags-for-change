import pandas as pd

PATH_HEADER = 'data/google_trends_raw/'

def create_paths_dict():
    """
    docstring
    """

    # TIER 1 FILE NAMES
    ukraine_trends = {
        'Ukraine conflict': 'google_trends_Ukraine_conflict.csv',
        'Ukraine war': 'google_trends_Ukraine_war.csv',
        'Russia ukraine': 'google_trends_Russia_Ukraine.csv',
        'Ukraine military': 'google_trends_Ukraine_military.csv',
        'Ukraine crisis': 'google_trends_Ukraine_crisis.csv',
        'Ukraine invasion': 'google_trends_Ukraine_invasion.csv'
    }
    india_trends = {
        'India protests': 'google_trends_India_protests.csv',
        'India riots': 'google_trends_India_riots.csv',
        'India demonstrations': 'google_trends_India_demonstrations.csv',
        'India unrest': 'google_trends_India_unrest.csv',
        'India strikes': 'google_trends_India_strikes.csv'
    }
    united_states_trends = {
        'US protests': 'google_trends_US_protests.csv',
        'United states protests': 'google_trends_United_States_protests.csv',
        'Protests america': 'google_trends_protests_America.csv',
        'Black lives matter': 'google_trends_Black_Lives_Matter.csv',
        'Capitol riots': 'google_trends_Capitol_riots.csv',
        'January 6': 'google_trends_January_6.csv'
    }
    myanmar_trends = {
        'Myanmar conflict': 'google_trends_Myanmar_conflict.csv',
        'Myanmar military': 'google_trends_Myanmar_military.csv',
        'Myanmar coup': 'google_trends_Myanmar_coup.csv',
        'Myanmar violence': 'google_trends_Myanmar_violence.csv'
    }
    mexico_trends = {
        'Mexico violence': 'google_trends_Mexico_violence.csv',
        'Mexico cartel': 'google_trends_Mexico_cartel.csv',
        'Mexico crime': 'google_trends_Mexico_crime.csv',
        'Mexico drug war': 'google_trends_Mexico_drug_war.csv'
    }
    syria_trends = {
        'Syria conflict': 'google_trends_Syria_conflict.csv',
        'Syria war': 'google_trends_Syria_war.csv',
        'Syria military': 'google_trends_Syria_military.csv',
        'Syria bombing': 'google_trends_Syria_bombing.csv'
    }
    brazil_trends = {
        'Brazil violence': 'google_trends_Brazil_violence.csv',
        'Brazil gangs': 'google_trends_Brazil_gangs.csv',
        'Brazil conflict': 'google_trends_Brazil_conflict.csv'
    }
    palestine_trends = {
        'Palestine conflict': 'google_trends_Palestine_conflict.csv',
        'Israel palestine': 'google_trends_Israel_Palestine.csv',
        'Gaza conflict': 'google_trends_Gaza_conflict.csv',
        'Gaza ceasefire': 'google_trends_Gaza_ceasefire.csv'
    }
    yemen_trends = {
        'Yemen conflict': 'google_trends_Yemen_conflict.csv',
        'Yemen war': 'google_trends_Yemen_war.csv',
        'Yemen violence': 'google_trends_Yemen_violence.csv',
        'Houthi yemen': 'google_trends_Houthi_Yemen.csv'
    }
    pakistan_trends = {
        'Pakistan protests': 'google_trends_Pakistan_protests.csv',
        'Pakistan violence': 'google_trends_Pakistan_violence.csv',
        'Pakistan demonstrations': 'google_trends_Pakistan_demonstrations.csv',
        'Pakistan unrest': 'google_trends_Pakistan_unrest.csv'
    }

    # TIER 2 FILE NAMES
    iraq_trends = {
        'Iraq conflict': 'google_trends_Iraq_conflict.csv',
        'Iraq war': 'google_trends_Iraq_war.csv',
        'Iraq military': 'google_trends_Iraq_military.csv'
    }
    france_trends = {
        'france protests': 'google_trends_France_protests.csv',
        'french demonstrations': 'google_trends_French_demonstrations.csv'
    }
    russia_trends = {
        'Russia military': 'google_trends_Russia_military.csv',
        'Russia conflict': 'google_trends_Russia_conflict.csv'
    }
    korea_trends = {
        'South Korea protests': 'google_trends_South_Korea_protests.csv',
        'Korea demonstrations': 'google_trends_Korea_demonstrations.csv'
    }
    turkey_trends = {
        'Turkey conflict': 'google_trends_Turkey_conflict.csv',
        'Turkey violence': 'google_trends_Turkey_violence.csv',
        'Turkey military': 'google_trends_Turkey_military.csv'
    }
    colombia_trends = {
        'Colombia violence': 'google_trends_Colombia_violence.csv',
        'Colombia conflict': 'google_trends_Colombia_conflict.csv'
    }
    lebanon_trends = {
        'Lebanon conflict': 'google_trends_Lebanon_conflict.csv',
        'Lebanon protests': 'google_trends_Lebanon_protests.csv',
        'Lebanon crisis': 'google_trends_Lebanon_crisis.csv'
    }
    nigeria_trends = {
        'Nigeria insurgency': 'google_trends_Nigeria_insurgency.csv',
        'Nigeria violence': 'google_trends_Nigeria_violence.csv',
        'Boko haram': 'google_trends_Boko_Haram.csv'
    }
    italy_trends = {
        'Italy protests': 'google_trends_Italy_protests.csv',
        'Italian demonstrations': 'google_trends_Italian_demonstrations.csv'
    }
    afghanistan_trends = {
        'Afghanistan conflict': 'google_trends_Afghanistan_conflict.csv',
        'Afghanistan military': 'google_trends_Afghanistan_military.csv',
        'Taliban': 'google_trends_Taliban.csv'
    }

    # TIER 3 FILE NAMES
    palestine_hashtags = {
        '#FreePalestine': 'google_trends_FreePalestine.csv',
        '#Gaza': 'google_trends_Gaza.csv',
        '#GazaCeasefire': 'google_trends_GazaCeasefire.csv',
        '#FreeGaza': 'google_trends_FreeGaza.csv'
    }
    ukraine_russia_hashtags = {
        '#UkraineWar': 'google_trends_UkraineWar.csv',
        '#StandWithUkraine': 'google_trends_StandWithUkraine.csv',
        '#SlavaUkraine': 'google_trends_SlavaUkraine.csv',
        '#RussiaUkraineWar': 'google_trends_RussiaUkraineWar.csv',
        '#StopPutin': 'google_trends_StopPutin.csv'
    }
    syria_hashtags = {
        '#SyriaWar': 'google_trends_SyriaWar.csv',
        '#Syria': 'google_trends_Syria.csv'
    }
    turkey_hashtags = {
        '#TurkishWomen': 'google_trends_TurkishWomen.csv'
    }
    yemen_hashtags = {
        '#TalkAboutYemen': 'google_trends_TalkAboutYemen.csv',
        '#YemenPeace': 'google_trends_YemenPeace.csv'
    }
    myanmar_hashtags = {
        '#WhatsHappeningInMyanmar': 'google_trends_WhatsHappeningInMyanmar.csv',
        '#MilkTeaAlliance': 'google_trends_MilkTeaAlliance.csv',
        '#POSCOStopSupportingSAC': 'google_trends_POSCOStopSupportingSAC.csv'
    }
    afghanistan_hashtags = {
        '#Afghanistan': 'google_trends_Afghanistan.csv',
        '#Taliban': 'google_trends_Taliban.csv'
    }
    iraq_hashtags = {
        '#Iraq': 'google_trends_Iraq.csv',
        '#IraqCeasefire': 'google_trends_IraqCeasefire.csv'
    }
    somalia_hashtags = {
        '#Somaliland': 'google_trends_Somaliland.csv',
        '#SomaliaHumanRights': 'google_trends_SomaliaHumanRights.csv'
    }
    india_pakistan_hashtags = {
        '#IndiaPakistan': 'google_trends_IndiaPakistan.csv',
        '#LiberateIndia': 'google_trends_LiberateIndia.csv',
        '#Pakistan': 'google_trends_Pakistan.csv',
        '#PakistanZindabad': 'google_trends_PakistanZindabad.csv'
    }
    united_states_hashtags = {
        '#StopGunViolence': 'google_trends_StopGunViolence.csv',
        '#BlackLivesMatter': 'google_trends_BlackLivesMatter.csv'
    }
    mexico_hashtags = {
        '#StandWithMexico': 'google_trends_StandWithMexico.csv',
        '#HopeForMexico': 'google_trends_HopeForMexico.csv'
    }
    brazil_hashtags = {
        '#SaveBrazil': 'google_trends_SaveBrazil.csv',
        '#RioCrisis': 'google_trends_RioCrisis.csv'
    }
    human_rights_hashtags = {
        '#NeverAgain': 'google_trends_NeverAgain.csv',
        '#Democracy': 'google_trends_Democracy.csv',
        '#FreeSpeech': 'google_trends_FreeSpeech.csv',
        '#HumanRights': 'google_trends_HumanRights.csv',
        '#FreePress': 'google_trends_FreePress.csv',
        '#YouthForDemocracy': 'google_trends_YouthForDemocracy.csv',
        '#Protest': 'google_trends_Protest.csv',
        '#DemocracyForAll': 'google_trends_DemocracyForAll.csv',
        '#NeverForget': 'google_trends_NeverForget.csv',
        '#Equality': 'google_trends_Equality.csv',
        '#Justice': 'google_trends_Justice.csv',
        '#Freedom': 'google_trends_Freedom.csv',
        '#Change': 'google_trends_Change.csv',
        '#FridaysForFuture': 'google_trends_FridaysForFuture.csv',
        '#PeopleNotProfit': 'google_trends_PeopleNotProfit.csv'
    }
    social_justice_hashtags = {
        '#MeToo': 'google_trends_MeToo.csv',
        '#StopFundingHate': 'google_trends_StopFundingHate.csv',
        '#WomensMarch': 'google_trends_WomensMarch.csv',
        '#TimesUp': 'google_trends_TimesUp.csv',
        '#GenerationEquality': 'google_trends_GenerationEquality.csv',
        '#MyBodyMyChoice': 'google_trends_MyBodyMyChoice.csv',
        '#ProChoice': 'google_trends_ProChoice.csv',
        '#LoveIsLove': 'google_trends_LoveIsLove.csv',
        '#TransRights': 'google_trends_TransRights.csv',
        '#EqualityForAll': 'google_trends_EqualityForAll.csv',
        '#TransRightsAreHumanRights': 'google_trends_TransRightsAreHumanRights.csv',
        '#EndSexualViolence': 'google_trends_EndSexualViolence.csv',
        '#WomensRights': 'google_trends_WomensRights.csv',
        '#LGBTQ+': 'google_trends_LGBTQ+.csv',
        '#GayPride': 'google_trends_GayPride.csv',
        '#ImmigrantRights': 'google_trends_ImmigrantRights.csv'
    }
    conflict_peace_hashtags = {
        '#NoWarCrimes': 'google_trends_NoWarCrimes.csv',
        '#Peace': 'google_trends_Peace.csv',
        '#NoWar': 'google_trends_NoWar.csv',
        '#StopWar': 'google_trends_StopWar.csv',
        '#StopTheWar': 'google_trends_StopTheWar.csv',
        '#HumanatarianCrisis': 'google_trends_HumanatarianCrisis.csv',
        '#RefugeeRelief': 'google_trends_RefugeeRelief.csv',
        '#PeaceForAll': 'google_trends_PeaceForAll.csv',
        '#Solidarity': 'google_trends_Solidarity.csv',
        '#Ceasefire': 'google_trends_Ceasefire.csv',
        '#CeasefireNOW': 'google_trends_CeasefireNOW.csv',
        '#StopGenocide': 'google_trends_StopGenocide.csv',
        '#Aid': 'google_trends_Aid.csv',
        '#StandWithPeace': 'google_trends_StandWithPeace.csv',
        '#SaveHumanity': 'google_trends_SaveHumanity.csv',
        '#EndViolence': 'google_trends_EndViolence.csv'
    }
    middle_east_hashtags = {
        '#MiddleEastCrisis': 'google_trends_MiddleEastCrisis.csv',
        '#MENA': 'google_trends_MENA.csv',
        '#FreeMiddleEast': 'google_trends_FreeMiddleEast.csv'
    }
    europe_hashtags = {
        '#EuropeanSolidarity': 'google_trends_EuropeanSolidarity.csv',
        '#EU': 'google_trends_EU.csv'
    }
    south_asia_hashtags = {
        '#HelpSouthAsia': 'google_trends_HelpSouthAsia.csv',
        '#UnifySouthAsia': 'google_trends_UnifySouthAsia.csv'
    }
    north_america_hashtags = {
        '#SaveNorthAmerica': 'google_trends_SaveNorthAmerica.csv',
        '#FreedomConvoy2022': 'google_trends_FreedomConvoy2022.csv'
    }


    # CONGREGATE!!!
    tier1_paths = {
        'ukraine': ukraine_trends,
        'india': india_trends,
        'united states': united_states_trends,
        'myanmar': myanmar_trends,
        'mexico': mexico_trends,
        'syria': syria_trends,
        'brazil': brazil_trends,
        'palestine': palestine_trends,
        'yemen': yemen_trends,
        'pakistan': pakistan_trends
    }

    tier2_paths = {
        'iraq': iraq_trends,
        'france': france_trends,
        'russia': russia_trends,
        'korea': korea_trends,
        'turkey': turkey_trends,
        'colombia': colombia_trends,
        'lebanon': lebanon_trends,
        'nigeria': nigeria_trends,
        'italy': italy_trends,
        'afghanistan': afghanistan_trends,
    }

    tier3_paths = {
        'country': {
            'palestine': palestine_hashtags,
            'ukraine russia': ukraine_russia_hashtags,
            'syria': syria_hashtags,
            'turkey': turkey_hashtags,
            'yemen': yemen_hashtags,
            'myanmar': myanmar_hashtags,
            'afghanistan': afghanistan_hashtags,
            'iraq': iraq_hashtags,
            'somalia': somalia_hashtags,
            'india pakistan': india_pakistan_hashtags,
            'united states': united_states_hashtags,
            'mexico': mexico_hashtags,
            'brazil': brazil_hashtags
            },
        'theme': {
            'human rights': human_rights_hashtags,
            'social justice': social_justice_hashtags,
            'conflict peace': conflict_peace_hashtags
            },
        'region': {
            'middle east': middle_east_hashtags,
            'europe': europe_hashtags,
            'south asia': south_asia_hashtags,
            'north america': north_america_hashtags
            }
    }

    for key, group in tier1_paths.items():
        for k, val in group.items():
            group[k] = PATH_HEADER + 'TIER1_COUNTRIES/' + val

    for key, group in tier2_paths.items():
        for k, val in group.items():
            group[k] = PATH_HEADER + 'TIER2_COUNTRIES/' + val

    for theme, group in tier3_paths.items():
        for key, cat in group.items():
            for k, val in cat.items():
                cat[k] = PATH_HEADER + 'TIER3_HASHTAGS/' + val

    return tier1_paths, tier2_paths, tier3_paths


def validate_paths(my_dict):
    """
    check if the paths work yuh
    """
    sum = 0
    for key, cat in my_dict.items():
        sum += len(cat)

        for k, filepath in cat.items():
            try:
                df = pd.read_csv(filepath, skiprows=1)
                print(f"✓ Success loading {k} in {key}")
            except Exception as e:
                print(f"    ✗ Error loading {k} in {key}: {e}")

    print(f"\nTOTAL FILES: {sum}\n")
    return sum


def validate_tier3(my_dict):
    """
    check if the paths work specifically for tier 3 yuh
    """
    sum = 0
    for theme, group in my_dict.items():
        for key, cat in group.items():
            sum += len(cat)

            for k, filepath in cat.items():
                try:
                    df = pd.read_csv(filepath, skiprows=1)
                    print(f"✓ Success loading {k} in {key} for {theme}")
                except Exception as e:
                    print(f"    ✗ Error loading {k} in {key} for {theme}")
    
    print(f"\nTOTAL FILES: {sum}\n")
    return sum
