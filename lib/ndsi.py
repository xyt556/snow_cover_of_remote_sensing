#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2019/5/15
@Author  : AnNing
"""
from __future__ import print_function

import os

import numpy as np

from lib.initialize import load_yaml_file

DUBUG = True
row = 210
col = 56

# Set Date Information
year_min = 2000
year_max = 2048
month_min = 1
month_max = 12
day_min = 1
day_max = 31
hour_min = 0
hour_max = 23


def no_none(iter_data):
    """
    判断输入数据中没有None
    :param iter_data:
    :return:
    """
    for data in iter_data:
        if data is None:
            return False
    return True


def ndsi(i_datetime=None,
         longitude=None,
         latitude=None,
         sensor_zenith=None,
         sensor_azimuth=None,
         solar_zenith=None,
         solar_azimuth=None,
         dems=None,
         sea_land_mask=None,
         cloud_mask=None,
         ref_01=None,
         ref_02=None,
         ref_03=None,
         ref_04=None,
         # ref_05=None,
         ref_06=None,
         ref_07=None,
         # ref_19=None,
         ref_26=None,
         tbb_20=None,
         # tbb_23=None,
         # tbb_29=None,
         tbb_31=None,
         tbb_32=None,

         ):
    # -------------------------------------------------------------------------
    # SolarZenith_MAX : MAXIMUM SOLAR ZENITH ANGLE, *1.0 DEGREE
    # solar_zenith_max = None

    # -------------------------------------------------------------------------
    # Date and Time
    # i_year = None
    # i_month = None
    # i_day = None
    # i_minute = None
    # n_year = None
    # n_month = None
    # n_day = None
    # n_hour = None
    # n_minute = None
    # n_second = None

    # -------------------------------------------------------------------------
    # r_lats = None  # LATITUDE
    # r_lons = None  # LONGITUDE
    # a_satz = None  # SATELLITE ZENITH ANGLE
    # a_sata = None  # SATELLITE AZIMUTH
    # a_sunz = None  # SOLAR ZENITH ANGLE
    # a_suna = None  # SOLAR AZIMUTH
    # r_dems = None  # DEM MASK
    # i_mask = None  # LANDCOVER MASK
    # i_cm = None  # Cloud MASK

    # -------------------------------------------------------------------------
    # cossl = None  # SOLAR-ZENITH-ANGLE-COSINE
    # glint = None  # SUN GLINT
    # lsm = None  # Mask For Water & Land
    # i_available = None  # Mask For Data to be used

    # -------------------------------------------------------------------------
    # ref_01 = None  # 0.645 um : Ref, NDVI
    # ref_02 = None  # 0.865 um : Ref, NDVI
    # ref_03 = None  # 0.470 um : Ref, NDVI
    # ref_04 = None  # 0.555 um : Ref, NDVI
    # ref_05 = None  # 1.640 um : Ref, NDVI
    # ref_06 = None  # 1.640 um : Ref, NDSI
    # ref_07 = None  # 2.130 um : Ref, NDSI
    # ref_19 = None  # 0.940 um : Ref, Vapour
    # ref_26 = None  # 1.375 um : Ref, Cirrus
    # tbb_20 = None  # 3.750 um : TBB, Temperature
    # tbb_31 = None  # 11.030 um : TBB, Temperature
    # tbb_32 = None  # 12.020 um : TBB, Temperature
    # -------------------------------------------------------------------------
    # ndvis = None  # R2-R1/R2+R1: R0.86,R0.65
    # ndsi_6 = None  # R4-R6/R4+R6: R0.55,R1.64
    # ndsi_7 = None  # R4-R7/R4+R7: R0.55,R2.13
    #
    # dr_16 = None  # R1-R6:       R0.86,R1.64
    # dr_17 = None  # R1-0.5*R7:   R0.86,R2.13
    #
    # dt_01 = None  # T20-T31:     T3.75-T11.0
    # dt_02 = None  # T20-T32:     T3.75-T12.0
    # dt_12 = None  # T31-T32:     T11.0-T12.0
    #
    # rr_21 = None  # R2/R1:       R0.86,R0.65
    # rr_46 = None  # R4/R6:       R0.55,R1.64
    # rr_47 = None  # R4/R7:       R0.55,R2.13
    #
    # dt_34 = None  # T20-T23:     T3.75-T4.05
    # dt_81 = None  # T29-T31:     T8.55-T11.0
    # dt_38 = None  # T20-T29:     T3.75-T8.55

    # -------------------------------------------------------------------------
    # Used for Masking Over-Estimation for snow by monthly snow pack lines.
    # LookUpTable For Monthly CHN-SnowPackLine (ZhengZJ, 2006)
    # Line:   Longitude from 65.0 to 145.0 (Step is 0.1 deg.)
    # Column: Month from Jan to Dec (Step is month)
    # Value:  Latitude (Unit is deg.)
    # r_mon_snow_line = np.array([])  # Monthly CHN-SnowPackLine

    # Used for judging low or water cloud by BT difference.
    # LookUpTable For T11-T12 (Saunders and Kriebel, 1988)
    # Line:   T11 from 250.0K to 310.0K (Step is 1.0K)
    # Column: Secant-SZA from 1.00 to 2.50 (Step is 0.01)
    # Value:  T11-T12 (Unit is K)
    # delta_bt_lut = np.array([])  # LookUpTable for BT11-BT12

    # Used for judging snow in forest by NDSI and NDVI.
    # LookUpTable For Snow in Forest , by NDVI-NDSI (Klein et al., 1998)
    # Line:   NDVI from 0.010 to 1.000 (Step is 0.01)
    # Column: NDSI from 0.01000 to 1.00000 (Step is 0.00001)
    # Value:  NDSI (Unit is null)
    # y_ndsi_x_ndvi = np.array([])  # LookUpTable for NDSI-NDVI

    # !!!!! Four Variables below should be USED TOGETHER.
    # !! R138R164LUT,R164T11_LUT,R164R138LUT,T11mT12R164LUT
    # !!   LookUpTable For FreshSnow&WaterIceCloud (ZhengZJ, 2006)
    # !!     (1)Line-R164T11_LUT:      T11 from 225.0 to 280.0 (Step is 0.1K)
    # !!        Column--R164T11_LUT:   R164 from 0.00000 to 0.24000 (No Step)
    # !!     (2)Line-T11mT12R164LUT:   R164 from 0.100 to 0.250 (Step is 0.001)
    # !!        Column-T11mT12R164LUT: T11mT12 from -40 to 130 (No Step)
    # !!     (3)Line-R138R164LUT:      R164 from 0.010 to 0.260 (Step is 0.001)
    # !!        Column-R138R164LUT:    R138 from 0.0020 to 0.3000 (No Step)
    # !!     (4)Line-R164R138LUT:      R138 from 0.000 to 0.550 (Step is 0.001)
    # !!        Column-R164R138LUT:    R164 from 0.1500 to 0.3000 (No Step)
    # y_r164_x_t11 = np.array([])  # LookUpTable For R164T11
    # y_t11_m_t12_x_r164 = np.array([])  # LookUpTable For T11mT12R164
    # y_r138_x_r164 = np.array([])  # LookUpTable For R138R164
    # y_r164_x_r138 = np.array([])  # LookUpTable For R164R138

    # -------------------------------------------------------------------------
    # Used for Reference of 11um Minimum Brightness Temperature.
    # ref_bt11um = None
    # ref_bt11um_slope_n = None
    # ref_bt11um_slope_s = None
    # ref_bt11um_offset_n = None
    # ref_bt11um_offset_s = None

    # a_low_t_lat = None  # Referential Latitude for BT11 LowThreshold
    # a_low_bt11 = None  # Referential Temp for BT11 LowThreshold
    # delta_t_low = None  # Referential Temporal Delta-Temp for BT11_Low
    # b_hai_t_lat = None  # Referential Latitude for BT11 HaiThreshold
    # b_hai_bt11 = None  # Referential Temp for BT11 HaiThreshold
    # delta_t_hai = None  # Referential Temporal Delta-Temp for BT11_Hai
    #
    # a_low_bt11_n = None
    # a_low_bt11_s = None
    # b_hai_bt11_n = None
    # b_hai_bt11_s = None

    # -------------------------------------------------------------------------
    # Used for Calculate and Store Xun number from 1 to 36 in a year.
    # f_xun_n = None
    # f_xun_s = None
    # i2_xun_num = None

    # -------------------------------------------------------------------------
    # i_step = np.array([])  # TEST-STEP
    # i_mark = np.array([])  # SNOW MAP

    # !!!!   VALUE = 255 : Fill Data--no Data expected For pixel
    # !!!!   VALUE = 254 : Saturated MODIS sensor detector
    # !!!!   VALUE = 240 : NATIONAL OR PROVINCIAL BOUNDARIES
    # !!!!   VALUE = 200 : Snow
    # !!!!   VALUE = 100 : Snow-Covered Lake Ice
    # !!!!   VALUE =  50 : Cloud Obscured
    # !!!!   VALUE =  39 : Ocean
    # !!!!   VALUE =  37 : Inland Water
    # !!!!   VALUE =  25 : Land--no snow detected
    # !!!!   VALUE =  11 : Darkness, terminator or polar
    # !!!!   VALUE =   1 : No Decision
    # !!!!   VALUE =   0 : Sensor Data Missing

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    print('Program : Make SNC')

    # -------------------------------------------------------------------------
    lib_path = os.path.abspath(os.path.dirname(__file__))
    cfg_path = os.path.join(os.path.dirname(lib_path), 'cfg')
    aid_path = os.path.join(os.path.dirname(lib_path), 'aid')
    name_list_swath_snc = os.path.join(cfg_path, 'ndsi_cfg.yaml')
    print('Config file : {}'.format(name_list_swath_snc))

    a = load_yaml_file(name_list_swath_snc)
    solar_zenith_max = float(a['SolarZenith_MAX'])
    inn_put_para_path = a['InnPut_ParaPath']

    inn_put_root_l01 = a['InnPut_Root_L01']
    inn_put_root_l02 = a['InnPut_Root_L02']
    inn_put_root_l03 = a['InnPut_Root_L03']
    inn_put_root_l11 = a['InnPut_Root_L11']
    inn_put_root_l12 = a['InnPut_Root_L12']
    inn_put_root_l13 = a['InnPut_Root_L13']
    inn_put_root_l14 = a['InnPut_Root_L14']

    inn_put_file_l01 = os.path.join(aid_path, inn_put_para_path, inn_put_root_l01)
    inn_put_file_l02 = os.path.join(aid_path, inn_put_para_path, inn_put_root_l02)
    inn_put_file_l03 = os.path.join(aid_path, inn_put_para_path, inn_put_root_l03)
    inn_put_file_l11 = os.path.join(aid_path, inn_put_para_path, inn_put_root_l11)
    inn_put_file_l12 = os.path.join(aid_path, inn_put_para_path, inn_put_root_l12)
    inn_put_file_l13 = os.path.join(aid_path, inn_put_para_path, inn_put_root_l13)
    inn_put_file_l14 = os.path.join(aid_path, inn_put_para_path, inn_put_root_l14)

    delta_bt_lut = np.loadtxt(inn_put_file_l01, skiprows=1)[:, 1:]

    r_mon_snow_line_temp = np.loadtxt(inn_put_file_l02, skiprows=1)[:, 1:]
    r_mon_snow_line = np.zeros((3601, 12, 2))
    r_mon_snow_line[:, :, 0] = r_mon_snow_line_temp[:, 0:24:2]
    r_mon_snow_line[:, :, 1] = r_mon_snow_line_temp[:, 1:24:2]

    y_ndsi_x_ndvi = np.loadtxt(inn_put_file_l03, skiprows=1)[:]

    y_r138_x_r164 = np.loadtxt(inn_put_file_l11, skiprows=1)[:]
    y_r164_x_t11 = np.loadtxt(inn_put_file_l12, skiprows=1)[:]
    y_r164_x_r138 = np.loadtxt(inn_put_file_l13, skiprows=1)[:]
    y_t11_m_t12_x_r164 = np.loadtxt(inn_put_file_l14, skiprows=1)[:]

    # -------------------------------------------------------------------------

    def get_ymdh(date):
        year, month, day, hour = date.strftime('%Y_%m_%d_%H').split('_')
        return int(year), int(month), int(day), int(hour)

    j_year, j_month, j_day, j_hour = get_ymdh(i_datetime)

    if (not year_min <= j_year <= year_max) or (not month_min <= j_month <= month_max) or \
            (not day_min <= j_day <= day_max) or (not hour_min <= j_hour <= hour_max):
        raise ValueError('Wrongly Time Setting. Please Retry:{}'.format(i_datetime))

    # -------------------------------------------------------------------------
    # Calculating the Number of Xun (means ten day).
    if j_day <= 10:
        i2_xun_num = 3 * (j_month - 1) + 1
    elif j_day > 20:
        i2_xun_num = 3 * (j_month - 1) + 3
    else:
        i2_xun_num = 3 * (j_month - 1) + 2

    if i2_xun_num == 21:
        f_xun_n = 0.
    elif i2_xun_num < 21:
        f_xun_n = np.abs(np.sin(np.pi * (i2_xun_num - 21 + 36) / 36))
    else:
        f_xun_n = np.abs(np.sin(np.pi * (i2_xun_num - 21) / 36))

    f_xun_s = np.sqrt(1.0 - f_xun_n ** 2)

    if DUBUG:
        print(' f_xun_n= ', f_xun_n, ' f_xun_s= ', f_xun_s)

    # -------------------------------------------------------------------------
    # Calculate Parameters (Slope & Offset) for Ref_BT11um
    a_low_t_lat = 57.
    a_low_bt11 = 243.
    delta_t_low = 15.
    b_hai_t_lat = 17.
    b_hai_bt11 = 270.
    delta_t_hai = 10.

    a_low_bt11_n = a_low_bt11 - f_xun_n * delta_t_low
    a_low_bt11_s = a_low_bt11 - f_xun_s * delta_t_low

    b_hai_bt11_n = b_hai_bt11 - f_xun_n * delta_t_hai
    b_hai_bt11_s = b_hai_bt11 - f_xun_s * delta_t_hai

    if DUBUG:
        print(' a_low_bt11= ', a_low_bt11, ' b_hai_bt11= ', b_hai_bt11)
        print(' a_low_bt11_n= ', a_low_bt11_n, ' a_low_bt11_s= ', a_low_bt11_s)
        print(' b_hai_bt11_n= ', b_hai_bt11_n, ' b_hai_bt11_s= ', b_hai_bt11_s)

    ref_bt11um_slope_n = (b_hai_bt11_n - a_low_bt11_n) / (b_hai_t_lat - a_low_t_lat)
    ref_bt11um_slope_s = (b_hai_bt11_s - a_low_bt11_s) / (b_hai_t_lat - a_low_t_lat)

    ref_bt11um_offset_n = a_low_bt11_n - ref_bt11um_slope_n * a_low_t_lat
    ref_bt11um_offset_s = a_low_bt11_s - ref_bt11um_slope_s * a_low_t_lat

    if DUBUG:
        print('ref_bt11um_slope_n', ref_bt11um_slope_n)
        print('ref_bt11um_slope_s', ref_bt11um_slope_s)
        print('ref_bt11um_offset_n', ref_bt11um_offset_n)
        print('ref_bt11um_offset_s', ref_bt11um_offset_s)

    # -------------------------------------------------------------------------
    # load row and col
    data_shape = ref_01.shape
    i_rows, i_cols = data_shape

    # -------------------------------------------------------------------------
    # Check Swath_Valid by Solar Zenith
    d_solar_zenith = solar_zenith
    i_sum_valid = np.logical_and(d_solar_zenith > 0, d_solar_zenith < solar_zenith_max).sum()
    if i_sum_valid < i_cols * 30:
        raise ValueError('Valid data is not enough.{} < {}'.format(i_sum_valid, i_cols * 30))

    # -------------------------------------------------------------------------
    # Read  FILE_GEO

    #  GET SensorZenith
    d_sensor_zenith = sensor_zenith
    index_valid = np.logical_and(d_sensor_zenith > 0, d_sensor_zenith < 90)
    d_sensor_zenith[index_valid] = d_sensor_zenith[index_valid] / 180 * np.pi
    d_sensor_zenith[~index_valid] = np.nan

    #  GET SensorAzimuth
    d_sensor_azimuth = sensor_azimuth
    index_valid = np.logical_and(d_sensor_azimuth > -360, d_sensor_azimuth < 360)
    d_sensor_azimuth[index_valid] = d_sensor_azimuth[index_valid] / 180 * np.pi
    d_sensor_azimuth[~index_valid] = np.nan

    #  GET SolarZenith
    d_solar_zenith = solar_zenith
    index_valid = np.logical_and(d_solar_zenith > 0, d_solar_zenith < 180)
    d_solar_zenith[index_valid] = d_solar_zenith[index_valid] / 180 * np.pi
    d_solar_zenith[~index_valid] = np.nan

    #  GET SolarAzimuth
    d_solar_azimuth = solar_azimuth
    index_valid = np.logical_and(d_solar_azimuth > -360, d_solar_azimuth < 360)
    d_solar_azimuth[index_valid] = d_solar_azimuth[index_valid] / 180 * np.pi
    d_solar_azimuth[~index_valid] = np.nan

    #  GET LATITUDE
    r_lats = latitude

    #  GET LONGITUDE
    r_lons = longitude

    #  GET Elevation
    r_dems = dems

    #  GET LandSea
    i_mask = sea_land_mask
    # -------------------------------------------------------------------------
    # MAKE SEA-LAND MASK
    # !!!!   NATIONAL OR PROVINCIAL BOUNDARIES.
    #
    # !!!!!!!!!!!!!!!!!!  LSM=0(1): Data IS ON WATER-BODY(LAND).  !!!!!!!!!!!!!!!!!!
    # c. !  iMASK = 0:  SHALLOW_OCEAN         !
    # c. !  iMASK = 1:  LAND                  !
    # c. !  iMASK = 2:  COASTLINE             !
    # c. !  iMASK = 3:  SHALLOW_INLAND_WATER  !
    # c. !  iMASK = 4:  EPHEMERAL_WATER       !
    # c. !  iMASK = 5:  DEEP_INLAND_WATER     !
    # c. !  iMASK = 6:  MODERATE_OCEAN        !
    # c. !  iMASK = 7:  DEEP_OCEAN            !
    land_condition = np.logical_or.reduce((i_mask == 1, i_mask == 2, i_mask == 3))
    sea_condition = np.logical_or(i_mask == 0, np.logical_and(i_mask > 3, i_mask < 8))

    i_lsm = np.full(data_shape, np.nan)
    i_lsm[land_condition] = 1  # 陆地
    i_lsm[sea_condition] = 0  # 海洋

    # -------------------------------------------------------------------------
    # GET Cloud Mask
    i_cm = cloud_mask

    # -------------------------------------------------------------------------
    #  INITIALIZATION
    i_mark = np.zeros(data_shape)
    i_step = np.zeros(data_shape)

    ref_lon = r_lons
    ref_lat = r_lats
    ref_dem = r_dems

    a_satz = d_sensor_zenith
    a_sata = d_sensor_azimuth
    a_sunz = d_solar_zenith
    a_suna = d_solar_azimuth

    # -------------------------------------------------------------------------
    # COMPUTE The SUN GLINT EAGLE
    temp = np.sin(a_sunz) * np.sin(a_satz) * np.cos(a_suna - a_sata) + np.cos(a_sunz) * np.cos(a_satz)
    temp[temp > 1] = 1
    temp[temp < -1] = -1
    glint = np.arccos(temp)

    # -------------------------------------------------------------------------
    lsm = i_lsm
    i_available = np.ones(data_shape, dtype=np.int8)

    index = np.isnan(a_sata)
    i_mark[index] = 255
    i_step[index] = 1
    i_available[index] = 0

    index = np.isnan(a_satz)
    i_mark[index] = 255
    i_step[index] = 2
    i_available[index] = 0

    index = np.isnan(a_sunz)
    i_mark[index] = 255
    i_step[index] = 3
    i_available[index] = 0

    index = np.isnan(a_suna)
    i_mark[index] = 255
    i_step[index] = 4
    i_available[index] = 0

    index = glint < 15 * np.pi / 180
    i_mark[index] = 255
    i_step[index] = 5
    i_available[index] = 0

    index = np.isnan(ref_lon)
    i_mark[index] = 255
    i_step[index] = 6
    i_available[index] = 0

    index = np.isnan(ref_lat)
    i_mark[index] = 255
    i_step[index] = 7
    i_available[index] = 0

    index = np.isnan(ref_dem)
    i_mark[index] = 255
    i_step[index] = 8
    i_available[index] = 0

    index = np.isnan(lsm)
    i_mark[index] = 255
    i_step[index] = 9
    i_available[index] = 0

    if ref_lat is not None:
        ref_lat_abs = np.abs(ref_lat)
    else:
        ref_lat_abs = None
    # -------------------------------------------------------------------------
    # COMPUTE The SUN GLINT EAGLE
    if ref_lat_abs is not None:
        ref_bt11um = np.full(data_shape, np.nan)

        index = ref_lat >= 0
        idx_ = np.logical_and(index, ref_lat_abs < b_hai_t_lat)
        ref_bt11um[idx_] = ref_bt11um_slope_n * np.abs(b_hai_t_lat) + ref_bt11um_offset_n

        idx_ = np.logical_and(index, ref_lat_abs > a_low_t_lat)
        ref_bt11um[idx_] = ref_bt11um_slope_n * np.abs(a_low_t_lat) + ref_bt11um_offset_n

        idx_ = np.logical_and.reduce((index, ref_lat_abs <= a_low_t_lat, ref_lat_abs >= b_hai_t_lat))
        ref_bt11um[idx_] = ref_bt11um_slope_n * ref_lat_abs[idx_] + ref_bt11um_offset_n

        index = ref_lat < 0
        idx_ = np.logical_and(index, ref_lat_abs < b_hai_t_lat)
        ref_bt11um[idx_] = ref_bt11um_slope_s * np.abs(b_hai_t_lat) + ref_bt11um_offset_s

        idx_ = np.logical_and(index, ref_lat_abs > a_low_t_lat)
        ref_bt11um[idx_] = ref_bt11um_slope_s * np.abs(a_low_t_lat) + ref_bt11um_offset_s

        idx_ = np.logical_and.reduce((index, ref_lat_abs >= b_hai_t_lat, ref_lat_abs <= a_low_t_lat))
        ref_bt11um[idx_] = ref_bt11um_slope_s * ref_lat_abs[idx_] + ref_bt11um_offset_s
    else:
        ref_bt11um = None

    # !!!!!!!!!!!!!!!!!!!!!!!!!!   QUALITY CONTROLLING   !!!!!!!!!!!!!!!!!!!!!!!!!!!
    #           iAvalible=1     !!  iAvalible=0(1): Data IS(NOT) USABLE.  !!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!   QUALITY CONTROLLING   !!!!!!!!!!!!!!!!!!!!!!!!!!!
    if ref_01 is not None:
        index = np.logical_or.reduce((np.isnan(ref_01), ref_01 <= 0, ref_01 >= 100))
        i_mark[index] = 255
        i_step[index] = 11
        i_available[index] = 0

    if ref_02 is not None:
        index = np.logical_or.reduce((np.isnan(ref_02), ref_02 <= 0, ref_02 >= 100))
        i_mark[index] = 255
        i_step[index] = 12
        i_available[index] = 0

    if ref_03 is not None:
        index = np.logical_or.reduce((np.isnan(ref_03), ref_03 <= 0, ref_03 >= 100))
        i_mark[index] = 255
        i_step[index] = 13
        i_available[index] = 0

    if ref_04 is not None:
        index = np.logical_or.reduce((np.isnan(ref_04), ref_04 <= 0, ref_04 >= 100))
        i_mark[index] = 255
        i_step[index] = 14
        i_available[index] = 0

    if ref_06 is not None:
        index = np.logical_or.reduce((np.isnan(ref_06), ref_06 <= 0, ref_06 >= 100))
        i_mark[index] = 255
        i_step[index] = 15
        i_available[index] = 0

    if ref_07 is not None:
        index = np.logical_or.reduce((np.isnan(ref_07), ref_07 <= 0, ref_07 >= 100))
        i_mark[index] = 255
        i_step[index] = 16
        i_available[index] = 0

    if tbb_20 is not None:
        index = np.logical_or.reduce((np.isnan(tbb_20), tbb_20 <= 170, tbb_20 >= 350))
        i_mark[index] = 255
        i_step[index] = 17
        i_available[index] = 0

    if tbb_31 is not None:
        index = np.logical_or.reduce((np.isnan(tbb_31), tbb_31 <= 170, tbb_31 >= 340))
        i_mark[index] = 255
        i_step[index] = 18
        i_available[index] = 0

    if tbb_32 is not None:
        index = np.logical_or.reduce((np.isnan(tbb_32), tbb_32 <= 170, tbb_32 >= 340))
        i_mark[index] = 255
        i_step[index] = 19
        i_available[index] = 0

    # # CORRECT SATURATION VALUE AFTER SOLAR ZENITH ANGLE CORRECTING.
    # cossl = 1.0
    # ref_01 = ref_01 * cossl
    # ref_02 = ref_01 * cossl
    # ref_03 = ref_01 * cossl
    # ref_04 = ref_01 * cossl
    # ref_06 = ref_01 * cossl
    # ref_07 = ref_01 * cossl
    # index = np.logical_or.reduce((ref_01 <= 0, ref_01 >= 100.0, ref_02 <= 0, ref_02 >= 100.0,
    #                               ref_03 <= 0, ref_03 >= 100.0, ref_04 <= 0, ref_04 >= 100.0,
    #                               ref_06 <= 0, ref_06 >= 100.0, ref_07 <= 0, ref_07 >= 100.0,
    #                               tbb_20 <= 170.0, tbb_20 >= 350.0, tbb_31 <= 170.0, tbb_31 >= 340.0,
    #                               tbb_32 <= 170.0, tbb_32 >= 340.0,))
    # i_mark[index] = 255
    # i_step[index] = 20
    # i_available[index] = 0

    # -------------------------------------------------------------------------
    # JUDGE & MARK  SNOW
    # !!!    iTAG For marking The case of Data
    # !!!!---- Notice ----!!!!    0: badData; 1: goodData unused; 2: goodData used.
    i_tag = np.zeros(data_shape, dtype=np.int8)

    idx_available = i_available == 1

    if no_none((ref_02, ref_01)):
        ndvis = (ref_02 - ref_01) / (ref_02 + ref_01)
    else:
        ndvis = None
    if no_none((ref_04, ref_06)):
        ndsi_6 = (ref_04 - ref_06) / (ref_04 + ref_06)
    else:
        ndsi_6 = None
    if no_none((ref_04, ref_07)):
        ndsi_7 = (ref_04 - ref_07) / (ref_04 + ref_07)
    else:
        ndsi_7 = None

    if no_none((ref_01, ref_06)):
        dr_16 = ref_01 - ref_06
    else:
        dr_16 = None
    if no_none((ref_01, ref_07)):
        dr_17 = ref_01 - 0.5 * ref_07
    else:
        dr_17 = None
    if no_none((tbb_20, tbb_31)):
        dt_01 = tbb_20 - tbb_31
    else:
        dt_01 = None
    if no_none((tbb_20, tbb_32)):
        dt_02 = tbb_20 - tbb_32
    else:
        dt_02 = None
    if no_none((tbb_31, tbb_32)):
        dt_12 = tbb_31 - tbb_32
    else:
        dt_12 = None

    if no_none((ref_02, ref_01)):
        rr_21 = ref_02 / ref_01
        rr_21[rr_21 > 100] = 100
    else:
        rr_21 = None
    if no_none((ref_04, ref_06)):
        rr_46 = ref_04 / ref_06
        rr_46[rr_46 > 100] = 100
    else:
        rr_46 = None

    # !!! 以下内容未用到
    # if no_none((ref_04, ref_07)):
    #     rr_47 = ref_04 / ref_07
    #     if rr_47 > 100.:
    #         rr_47 = 100
    # else:
    #     rr_47 = None
    #
    # if no_none((tbb_20, tbb_23)):
    #     dt_34 = tbb_20 - tbb_23
    # else:
    #     dt_34 = None
    # if no_none((tbb_29, tbb_31)):
    #     dt_81 = tbb_29 - tbb_31
    # else:
    #     dt_81 = None
    # if no_none((tbb_20, tbb_29)):
    #     dt_38 = tbb_20 - tbb_29
    # else:
    #     dt_38 = None
    # ##############################################################################
    # ！！！！！！！！！！！！！！！！！！ DEBUG ！！！！！！！！！！！！！！！！！！
    # ##############################################################################
    if DUBUG:
        print('row=', row)
        print('col=', col)
        print('ref_01=', ref_01[row, col])
        print('ref_02=', ref_02[row, col])
        print('ref_03=', ref_03[row, col])
        print('ref_04=', ref_04[row, col])
        print('ref_06=', ref_06[row, col])
        print('ref_07=', ref_07[row, col])
        print('ref_26=', ref_26[row, col])
        print('tbb_20=', tbb_20[row, col])
        print('tbb_31=', tbb_31[row, col])
        print('longitude=', longitude[row, col])
        print('latitude=', latitude[row, col])
        print('sensor_zenith=', sensor_zenith[row, col])
        print('sensor_azimuth=', sensor_azimuth[row, col])
        print('solar_zenith=', solar_zenith[row, col])
        print('solar_azimuth=', solar_azimuth[row, col])
        print('dems=', dems[row, col])
        print('sea_land_mask=', sea_land_mask[row, col])
        print('ndvis=', ndvis[row, col])
        print('ndsi_6=', ndsi_6[row, col])
        print('ndsi_7=', ndsi_7[row, col])
        print('dr_16=', dr_16[row, col])
        print('dr_17=', dr_17[row, col])
        print('dt_01=', dt_01[row, col])
        print('dt_02=', dt_02[row, col])
        print('dt_12=', dt_12[row, col])
        print('rr_21=', rr_21[row, col])
        print('rr_46=', rr_46[row, col])

    # ##############################################################################
    # ！！！！！！！！！！！！！！！！！！开始处理
    # ##############################################################################
    i_tag[idx_available] = 1

    judge = np.full(data_shape, True, dtype=np.bool)

    # !!! 20190614 暂时不用NDVI去判断水体和陆地
    # !!! WHEN LAND-WATER MASK IS WRONG
    # idx_lsm = np.logical_and(idx_available, ndvis > 0.9)
    # lsm[idx_lsm] = 1
    # idx_lsm = np.logical_and(idx_available, ndvis < -0.9)
    # lsm[idx_lsm] = 0

    # !!!========================================================================!!!
    # !!!========================================================================!!!
    # !!!!                TESTING For WATER-BODY-PIXEL  LSM = 0                 !!!!
    # !!!========================================================================!!!
    # !!!========================================================================!!!
    # !!!---!!!---!!!   Notice  :  Test on Water Body ( LSM = 0 )    !!!---!!!---!!!
    # !!!!   TESTING For WATER-BODY ( INNER LAND, Except Glint Area )
    # !!!!!   TESTING For WATER-BODY ( OCEAN, Except Glint Area )
    idx_ocean = np.logical_and(idx_available, lsm == 0)

    # !!!!   TESTING For WATER-BODY ( INNER LAND, Except Glint Area )
    # !!!!!   TESTING For WATER-BODY ( OCEAN, Except Glint Area )
    if no_none((rr_46, ndsi_6, tbb_31)):
        idx_ = np.logical_or.reduce((rr_46 > 2., ndsi_6 > 0.38, tbb_31 > 274.5))
        idx_ = np.logical_and(idx_ocean, judge, idx_)
        i_mark[idx_] = 39
        i_step[idx_] = 20
        i_tag[idx_] = 2
        judge[idx_] = False

        idx_ = np.logical_and(idx_, ref_dem > 0)
        i_mark[idx_] = 37

    # !!!!   TESTING For WATER-BODY ( INNER LAND, Except Glint Area )
    # !!!!!   TESTING For WATER-BODY ( OCEAN, Except Glint Area )
    if no_none((ref_01, ref_02, ref_06, tbb_31)):
        idx_ = np.logical_and.reduce((ref_02 < 11., ref_06 > 4., tbb_31 > 274.5))
        idx_ = np.logical_or.reduce((ref_01 < 7.5, ref_02 < 6., idx_))
        idx_ = np.logical_and(idx_ocean, judge, idx_)
        i_mark[idx_] = 39
        i_step[idx_] = 21
        i_tag[idx_] = 2
        judge[idx_] = False

        idx_ = np.logical_and(idx_, ref_dem > 0)
        i_mark[idx_] = 37

    # !!!!   CERTAIN CLOUD-1 (High Cloud ; Ice Cloud ; Cold Cloud)
    # !!!!   Temperature_Test by Referential BT11 Threshold
    # !!!!   Cirrus_Test by Referential R1.38 Threshold
    if no_none((ref_lat_abs, tbb_31, ref_26, ref_bt11um)):
        ref_bt11um_copy = ref_bt11um.copy()
        ref_bt11um_copy[ref_bt11um_copy + 5 > 254.15] = 245.15
        idx_ = np.logical_and.reduce((ref_lat_abs > 42, ref_lat < 60, tbb_31 < ref_bt11um_copy))
        idx_ = np.logical_or(ref_26 > 7.5, idx_)
        idx_ = np.logical_and(idx_ocean, judge, idx_)
        i_mark[idx_] = 50
        i_step[idx_] = 22
        i_tag[idx_] = 2
        del ref_bt11um_copy

    # !!!!   CERTAIN CLOUD-2 (Middle or Low Level Cloud, Except Glint Area)
    if no_none((ref_06, tbb_20, dt_02, rr_46, ndsi_6)):
        idx1_ = np.logical_and(ref_06 > 8.5, tbb_20 > 278.5)
        idx2_ = np.logical_and(dt_02 > 9.5, rr_46 < 8.)
        idx_ = np.logical_or.reduce((idx1_, idx2_, ndsi_6 < 0.5))
        idx_ = np.logical_and(idx_ocean, judge, idx_)
        i_mark[idx_] = 50
        i_step[idx_] = 23
        i_tag[idx_] = 2
        judge[idx_] = False
        del idx1_, idx2_

    if no_none((ndsi_6, ndvis, tbb_31, dr_16, ref_01, ref_06)):
        idx_ = np.logical_and.reduce((ndsi_6 > 0.6, ndvis > -0.15, tbb_31 < 273.5, dr_16 > 20., ref_01 > 25.,
                                      ref_06 > 4., ref_06 < 20.))
        idx_ = np.logical_and(idx_ocean, judge, idx_)
        i_mark[idx_] = 200
        i_step[idx_] = 24
        i_tag[idx_] = 2

    if no_none((ndsi_6, ndvis, tbb_31, dr_16, ref_01, ref_06, rr_46)):
        idx_ = np.logical_and.reduce((ndsi_6 > 0.6, ndvis < -0.03, tbb_31 < 274.5, dr_16 > 9., dr_16 < 60.,
                                      ref_01 > 10., ref_01 < 60., ref_06 < 10., rr_46 > 10.))
        idx_ = np.logical_and(idx_ocean, judge, idx_)
        i_mark[idx_] = 100
        i_step[idx_] = 25
        i_tag[idx_] = 2

    # !!!------------------------------------------------------------------------!!!
    # !!!!    Monthly_SnowPackLine_LUT CLOUD-TEST For The REHANDLED DOT
    # !!!------------------------------------------------------------------------!!!
    # 监测雪线
    # !
    # !     Eliminate Snow by Monthly_SnowPackLine_LUT Cloud-Test for rehandled pixel
    # !
    if no_none((ref_lon, ref_lat)):
        _condition = np.logical_or(i_mark == 200, i_mark == 100)

        i_nor_s = np.zeros(data_shape, dtype=np.int8)
        i_nor_s[ref_lat > 0] = 1
        _condition2 = np.abs(r_mon_snow_line[np.round((ref_lon + 180) * 10).astype(np.int16),
                                             int(j_month - 1), i_nor_s]) > abs(ref_lat)
        idx_ = np.logical_and.reduce((idx_ocean, judge, _condition, _condition2))
        i_mark[idx_] = 50
        i_step[idx_] = 26
        i_tag[idx_] = 2
        judge[idx_] = False
        del _condition2

        idx_ = np.logical_and.reduce((idx_ocean, judge, np.abs(ref_lat) < 30, _condition))
        i_mark[idx_] = 50
        i_step[idx_] = 27
        i_tag[idx_] = 2
        judge[idx_] = False

        idx_ = np.logical_and.reduce((idx_ocean, judge, _condition))
        judge[idx_] = False

    # !!!!   TESTING For WATER-BODY FROM UNKOWN PIXELS( INNER LAND, Except Glint Area )
    # !!!!   TESTING For WATER-BODY FROM UNKOWN PIXELS ( OCEAN, Except Glint Area )
    if no_none((ref_06, dt_02, rr_46)):
        idx_ = np.logical_and.reduce((idx_ocean, judge, ref_06 < 6, dt_02 < 5, rr_46 > 3))
        i_mark[idx_] = 39
        i_step[idx_] = 28
        i_tag[idx_] = 2
        judge[idx_] = False

    idx_ = np.logical_and(idx_ocean, judge)
    i_mark[idx_] = 1
    i_step[idx_] = 30
    i_tag[idx_] = 2
    judge[idx_] = False

    del idx_ocean
    # !!!========================================================================!!!
    # !!!========================================================================!!!
    # !!!!                   TESTING For LAND-PIXEL  LSM = 1                    !!!!
    # !!!========================================================================!!!
    # !!!========================================================================!!!
    idx_land = np.logical_and(idx_available, lsm == 1)
    # !!!!   TESTING For Clear Land ( For Forest )
    # !!!!   CERTAIN
    if no_none((tbb_31, ndvis)):
        idx_ = np.logical_and.reduce((idx_land, judge, tbb_31 > 278, ndvis > 0.2))
        i_mark[idx_] = 25
        i_step[idx_] = 31
        i_tag[idx_] = 2
        judge[idx_] = False

    # !!!!   TESTING For Clear Land ( Including some Dust Storm above Desert )
    # !!!!   CERTAIN
    if ndsi_6 is not None:
        idx_ = np.logical_and.reduce((idx_land, judge, ndsi_6 < -0.2))
        i_mark[idx_] = 25
        i_step[idx_] = 32
        i_tag[idx_] = 2
        judge[idx_] = False

    # !!!---!!!---!!!      Notice  :  Test on Land ( LSM = 1 )       !!!---!!!---!!!
    if no_none((dt_12, ndsi_6, dt_01)):
        idx_temp = np.logical_and(dt_12 < -0.1, ndsi_6 < 0.08)
        # !!!!   TESTING For Cloud ( Including some Dust Storm above Desert )
        idx_ = np.logical_and.reduce((idx_land, judge, idx_temp, ref_26 > 5))
        i_mark[idx_] = 50
        i_step[idx_] = 34
        i_tag[idx_] = 2
        judge[idx_] = False

        # !!!!   TESTING For Clear Land ( Including some Dust Storm above Desert )
        # !!!!   TESTING For Clear Land ( Including some Dust Storm above Desert )
        idx_ = np.logical_and.reduce((idx_land, judge, idx_temp, dt_01 < 28))
        i_mark[idx_] = 25
        i_step[idx_] = 34
        i_tag[idx_] = 2
        judge[idx_] = False
        # !!!!   TESTING For Cloud ( Including some Dust Storm above Desert )
        idx_ = np.logical_and.reduce((idx_land, judge, idx_temp, dt_01 >= 28))
        i_mark[idx_] = 25
        i_step[idx_] = 35
        i_tag[idx_] = 2
        judge[idx_] = False

    # !!!!   TESTING For Clear Land ( Including Desert and Non-High-LAT Vegetation )
    # !!!!   CERTAIN
    if no_none((dr_16,)):
        idx_ = np.logical_and.reduce((idx_land, judge, dr_16 < -7.5))
        i_mark[idx_] = 25
        i_step[idx_] = 36
        i_tag[idx_] = 2
        judge[idx_] = False

    # !!!!   TESTING For Snow on Land ( Certainly Snow by  )
    # !!!!   CERTAIN
    if no_none((rr_46, ref_01, tbb_31)):
        idx_ = np.logical_and.reduce((idx_land, judge, rr_46 > 5.5, ref_01 > 65, tbb_31 > 240.5, tbb_31 < 276.5))
        i_mark[idx_] = 200
        i_step[idx_] = 37
        i_tag[idx_] = 2
        judge[idx_] = False

    # !!!!   TESTING For Cloud ( mid-lower Cloud AFTER Desert is marked )
    if no_none((ref_dem, ref_06, ref_01, ref_02)):
        idx_ = np.logical_and.reduce((idx_land, judge, ref_dem < 1800, ref_06 > 28, ref_01 > 34, ref_02 > 44))
        i_mark[idx_] = 50
        i_step[idx_] = 38
        i_tag[idx_] = 2
        judge[idx_] = False

    if no_none((ref_dem, dt_01)):
        idx_ = np.logical_and.reduce((idx_land, judge, ref_dem < 1800, dt_01 > 20.5))
        i_mark[idx_] = 50
        i_step[idx_] = 39
        i_tag[idx_] = 2
        judge[idx_] = False

    if no_none((ref_dem, ref_06, ref_dem, ref_01, ref_02)):
        idx_ = np.logical_and.reduce((idx_land, judge, ref_dem >= 1800, ref_06 > (28. + (ref_dem - 1800.) * 0.004),
                                      ref_01 > 34, ref_02 > 44))
        i_mark[idx_] = 50
        i_step[idx_] = 40
        i_tag[idx_] = 2
        judge[idx_] = False

    if no_none((ref_dem, dt_01)):
        idx_ = np.logical_and.reduce((idx_land, judge, ref_dem >= 1800, dt_01 > (20.5 + (ref_dem - 1800.) * 0.002)))
        i_mark[idx_] = 50
        i_step[idx_] = 41
        i_tag[idx_] = 2
        judge[idx_] = False

    if no_none((tbb_31, tbb_32, a_satz, ndsi_6)):
        idx_temp = np.logical_or.reduce((tbb_31 < 170, tbb_31 > 335, tbb_32 < 170, tbb_32 > 335, a_satz > 8,
                                         ndsi_6 > 0.5))
        test_dtb = tbb_31 - tbb_32
        i_test_t11 = np.round(tbb_31).astype(np.int16)
        i_test_t11[i_test_t11 <= 250] = 250
        i_test_t11[i_test_t11 >= 310] = 310
        sec_sza = 100. / np.cos(a_satz)
        i_sec_sza = np.round(sec_sza).astype(np.int16)
        i_sec_sza[i_sec_sza >= 250] = 250

        idx_ = np.logical_and.reduce((idx_land, judge, ~idx_temp))
        idx_ = np.logical_and(idx_,
                              test_dtb > delta_bt_lut[np.round(i_test_t11 - 250).astype(np.int16), i_sec_sza - 100])
        i_mark[idx_] = 50
        i_step[idx_] = 42
        i_tag[idx_] = 2
        judge[idx_] = False
        del idx_temp

    # !!!!   CERTAIN CLOUD-1 (High Cloud ; Ice Cloud ; Cold Cloud)
    # !!!!   Temperature_Test by Referential BT11 Threshold
    # !!!!   Cirrus_Test by Referential R1.38 Threshold
    if no_none((ref_dem, ref_bt11um, tbb_31, ref_lat_abs)):
        compared_t11_hai_lat_a = ref_bt11um + 8. - ref_dem / 1000.
        compared_t11_hai_lat_b = 250. - ref_dem / 1000.
        compared_t11_hai_lat = np.minimum(compared_t11_hai_lat_a, compared_t11_hai_lat_b)

        compared_t11_low_lat_a = ref_bt11um + 12. - ref_dem / 400.
        compared_t11_low_lat_b = 260. - ref_dem / 400.
        compared_t11_low_lat = np.maximum(compared_t11_low_lat_a, compared_t11_low_lat_b)

        idx_1 = np.logical_and.reduce((ref_lat_abs >= 40, ref_lat_abs <= 57, tbb_31 < compared_t11_hai_lat))
        idx_2 = np.logical_and.reduce((ref_lat_abs >= 17, ref_lat_abs <= 40, tbb_31 < compared_t11_low_lat))
        idx_ = np.logical_or(idx_1, idx_2)
        idx_ = np.logical_and.reduce((idx_land, judge, idx_))
        i_mark[idx_] = 50
        i_step[idx_] = 43
        i_tag[idx_] = 2
        judge[idx_] = False
        del idx_1, idx_2
        del compared_t11_hai_lat_a, compared_t11_hai_lat_b, compared_t11_hai_lat
        del compared_t11_low_lat_a, compared_t11_low_lat_b, compared_t11_low_lat

    # !!!!   CLOUD-1 (High Cloud ; Ice Cloud ; Cold Cloud)
    if no_none((ref_dem, ref_26, dt_01, tbb_31, ndsi_6, ref_bt11um)):
        compared_ref26 = 14.5 + ref_dem / 500.
        idx_ = np.logical_or(np.logical_and(ref_26 > compared_ref26, dt_01 > 21),
                             np.logical_and.reduce((
                                 ref_26 > compared_ref26 - 7, tbb_31 < ref_bt11um + 8, ndsi_6 > -0.11)))
        i_mark[idx_] = 50
        i_step[idx_] = 44
        i_tag[idx_] = 2
        judge[idx_] = False

    # !!!!!   TESTING For LAND WITH CLEAR SKY
    # !!!!!   CERTAIN
    if no_none((ndvis, ndsi_6, ndsi_7, rr_21, dr_17, dr_16)):
        idx_1 = np.logical_and(ndvis > 0.24, ndsi_6 < 0.14)
        idx_2 = np.logical_and(rr_21 > 1.42, ndsi_6 < 0.145)
        idx_3 = np.logical_and(dr_17 < 14, ndsi_6 < 0.135)
        idx_ = np.logical_or.reduce((idx_1, idx_2, idx_3, ndsi_6 < -0.21, ndsi_7 < -0.08, dr_16 < -9.8))
        idx_ = np.logical_and.reduce((idx_land, judge, idx_))
        i_mark[idx_] = 25
        i_step[idx_] = 45
        i_tag[idx_] = 2
        del idx_1, idx_2, idx_3

    # !!!!   TESTING For Clear Land ( For Forest , small number )
    # !!!!   CERTAIN
    if no_none((ndvis, ndsi_6, rr_21, dr_16)):
        idx_1 = np.logical_and(ndvis > 0.24, ndsi_6 < 0.15)
        idx_2 = np.logical_and(rr_21 > 1.4, ndsi_6 < 0.15)
        idx_ = np.logical_or.reduce((idx_1, idx_2, ndsi_6 < -0.21, dr_16 < -9.5))
        idx_ = np.logical_and.reduce((idx_land, judge, idx_))
        i_mark[idx_] = 25
        i_step[idx_] = 46
        i_tag[idx_] = 2
        judge[idx_] = False
        del idx_1, idx_2

    # !!!!   TESTING For Snow in Forest by NDVI-NDSI6-T11
    # !!!------------------------------------------------------------------------!!!
    # !!!!    NDVI_NDSI_LUT SNOW-TEST
    # !!!------------------------------------------------------------------------!!!
    if no_none((ndvis, tbb_31, ndsi_6)):
        idx_ = np.logical_and.reduce((ndvis > 0.1, tbb_31 < 277,
                                      ndsi_6 > y_ndsi_x_ndvi[np.round(ndvis * 100).astype(np.int16), 1]))
        idx_ = np.logical_and.reduce((idx_land, judge, idx_))
        i_mark[idx_] = 200
        i_step[idx_] = 47
        i_tag[idx_] = 2
        judge[idx_] = False
        del idx_

    # !!!!   TESTING For SNOW ON LAND ( For FOREST-SNOW )
    # !!!!   SNOW-0
    if no_none((ndsi_6, ref_lat_abs, tbb_31, ndvis, ref_02, ref_06)):
        idx_ = np.logical_and.reduce((ndsi_6 > 0.18, ref_lat_abs > 36, tbb_31 > 240.15, tbb_31 < 272.15,
                                      ndvis > 0.16, ref_02 > 20, ref_06 < 17))
        idx_ = np.logical_and.reduce((idx_land, judge, idx_))
        i_mark[idx_] = 200
        i_step[idx_] = 48
        i_tag[idx_] = 2
        judge[idx_] = False
        del idx_

    idx_ = np.logical_and(idx_land, judge, i_mark == 25)
    judge[idx_] = False
    del idx_

    # !!!!   TESTING For SNOW ON LAND ( For Thawy Snow )
    # !!!!   SNOW-1
    if no_none((ref_dem, ndsi_6, tbb_20, tbb_31, dt_01, ref_01, ref_06, ref_26)):
        idx_ = np.logical_and.reduce((ref_dem > 2000, ndsi_6 > 0.33, tbb_20 > 266.15, tbb_20 < 285.15,
                                      tbb_31 > 264.15, tbb_31 < 275.15, dt_01 > 6.5, dt_01 < 21,
                                      ref_01 > 41, ref_01 < 79, ref_06 > 12.5, ref_06 < 24.5,
                                      ref_26 > 9.5, ref_26 < 17))
        i_mark[idx_] = 200
        i_step[idx_] = 49
        i_tag[idx_] = 2
        judge[idx_] = False
        del idx_

    # !!!!    TESTING For Thin-Snow by Using R01-R06-NDSI6
    # !!!!   SNOW-2
    # if no_none((ref_bt11um, ref_dem, tbb_31, ref_01, ref_06, ndsi_6)):
    #     ref_bt11um_min = ref_bt11um.copy()
    #     ref_bt11um_min[ref_bt11um_min > 265.15] = 265.15
    #     idx_ = np.logical_and.reduce((ref_dem > 750, tbb_31 > ref_bt11um_min, tbb_31 < 282, ref_01 > 20,
    #                                   ref_01 < 55, ref_06 > 10, ref_06 < 24, ndsi_6 > (0.68 - 0.0262 * ref_06),
    #                                   ndsi_6 > (-0.33 + 0.0164 * ref_01)))
    #     idx_ = np.logical_and.reduce((idx_land, judge, idx_))
    #     i_mark[idx_] = 200
    #     i_step[idx_] = 50
    #     i_tag[idx_] = 2
    #     judge[idx_] = False
    #     del idx_

    # !!!!   TESTING For SNOW ON LAND
    # !!!!   SNOW-3
    if no_none((ref_bt11um, ref_lat, ref_lat_abs, ref_dem, rr_46, tbb_31)):
        snow_ref_bt11um = np.full(data_shape, 268, dtype=np.float32)
        snow_ref_bt11um[ref_lat > 40] = ref_bt11um[ref_lat > 40] + 5.
        idx_ = np.logical_and(ref_lat_abs > 20, ref_lat_abs < 40)
        snow_ref_bt11um[idx_] = ref_bt11um[idx_] + 18 - ref_dem[idx_] / 800
        idx_1 = np.logical_and.reduce((idx_land, judge, rr_46 > 3.1, snow_ref_bt11um < tbb_31, tbb_31 < 278))
        idx_ = np.logical_and(idx_1, ref_lat_abs > 20)
        i_mark[idx_] = 200
        i_step[idx_] = 51
        i_tag[idx_] = 2
        judge[idx_] = False
        del idx_

        idx_ = np.logical_and(idx_1, ~(ref_lat_abs > 20))
        i_mark[idx_] = 50
        i_step[idx_] = 52
        i_tag[idx_] = 2
        judge[idx_] = False
        del idx_1

    # !!!!   TESTING For SNOW ON LAND
    # !!!!   SNOW-4
    if no_none((dr_16, ref_06, tbb_31, rr_46, dt_02, ref_02, ref_bt11um)):
        idx_ = np.logical_and.reduce((idx_land, judge, dr_16 > 10, ref_06 < 19.5, tbb_31 < 276.15,
                                      rr_46 > 1.5, 2.45 < dt_02, dt_02 < 15, ref_02 > 26,
                                      tbb_31 > ref_bt11um + 5.0))
        i_mark[idx_] = 200
        i_step[idx_] = 53
        i_tag[idx_] = 2
        del idx_

    # !!!!   TESTING For SNOW ON LAND
    # !!!!   SNOW-5
    if no_none((ndsi_6, ref_bt11um, tbb_31)):
        idx_ = np.logical_and.reduce((idx_land, judge, ndsi_6 > 0.52, tbb_31 > ref_bt11um + 2, tbb_31 < 278))
        i_mark[idx_] = 200
        i_step[idx_] = 54
        i_tag[idx_] = 2
        del idx_

    if no_none((ndsi_6, tbb_31, ndvis, ref_02)):
        idx_ = np.logical_and.reduce((idx_land, judge, ndsi_6 > 0.12, ndsi_6 < 0.52, tbb_31 > ref_bt11um,
                                      tbb_31 < 276.15, ndvis > 0.16, ref_02 > 26))
        i_mark[idx_] = 200
        i_step[idx_] = 55
        i_tag[idx_] = 2
        del idx_

    # !!!!   TESTING For SNOW ON LAND
    # !!!!   Eliminate_Snow-1
    # !!!------------------------------------------------------------------------!!!
    # !!!!    IceCloud_Overlay_WaterCloud_LUT CLOUD-TEST For The REHANDLED DOT
    # !!!------------------------------------------------------------------------!!!
    if no_none((ref_dem, ref_06, tbb_31, ref_26)):
        idx_ = np.logical_and.reduce((i_mark == 200, ref_dem < 3000, ndsi_6 > 0.38, ref_06 > 10, ref_06 < 25,
                                      ref_26 > 0.01, ref_26 < 55, tbb_31 > 235, tbb_31 < 275))
        ice_cloud_sums = np.zeros(data_shape, dtype=np.int8)

        idx_1 = np.logical_and(idx_, np.isfinite(ref_06))
        y_r138_x_r164_first = y_r138_x_r164[0, 0]
        idx_2 = ref_26[idx_1] * 100 > y_r138_x_r164[
            (np.round(ref_06[idx_1] * 10) - y_r138_x_r164_first).astype(np.int32), 1]
        ice_cloud_sums[idx_1][idx_2] += 1

        y_t11_m_t12_x_r164_first = y_t11_m_t12_x_r164[0, 0]
        idx_2 = dt_12[idx_1] * 100. > y_t11_m_t12_x_r164[
            (np.round(ref_06[idx_1] * 10) - y_t11_m_t12_x_r164_first).astype(np.int32), 1]
        ice_cloud_sums[idx_1][idx_2] += 1

        idx_1 = np.logical_and(idx_, np.isfinite(tbb_31))
        y_r164_x_t11_first = y_r164_x_t11[0, 0]
        idx_2 = ref_06[idx_1] * 100 > y_r164_x_t11[
            (np.round(tbb_31[idx_1] * 10) - y_r164_x_t11_first).astype(np.int32), 1]
        ice_cloud_sums[idx_1][idx_2] += 1

        idx_1 = np.logical_and(idx_, np.isfinite(ref_26))
        y_r164_x_r138_first = y_r164_x_r138[0, 0]
        idx_2 = ref_06[idx_1] * 100 > y_r164_x_r138[
            (np.round(ref_26[idx_1] * 10) - y_r164_x_r138_first).astype(np.int32), 1]
        ice_cloud_sums[idx_1][idx_2] += 1
        idx_ = ice_cloud_sums > 2
        i_mark[idx_] = 50
        i_step[idx_] = 56
        i_tag[idx_] = 2
        judge[idx_] = False

    # !!!!   TESTING For SNOW ON LAND
    # !!!!   Eliminate_Snow-2
    # !!!------------------------------------------------------------------------!!!
    # !!!!    Monthly_SnowPackLine_LUT CLOUD-TEST For The REHANDLED DOT
    # !!!------------------------------------------------------------------------!!!
    if no_none((ref_lon, ref_lat)):
        _condition = np.logical_or(i_mark == 200, i_mark == 100)

        i_nor_s = np.zeros(data_shape, dtype=np.int8)
        i_nor_s[ref_lat > 0] = 1
        _condition2 = np.abs(r_mon_snow_line[np.round((ref_lon + 180) * 10).astype(np.int16),
                                             int(j_month - 1), i_nor_s]) > abs(ref_lat)
        idx_ = np.logical_and.reduce((idx_land, judge, _condition, _condition2))
        i_mark[idx_] = 50
        i_step[idx_] = 57
        i_tag[idx_] = 2
        judge[idx_] = False
        del _condition2, idx_

        idx_ = np.logical_and.reduce((idx_land, judge, i_mark == 200))
        judge[idx_] = False
        del _condition, idx_

    # !!!!   TESTING For CLOUD
    if no_none((ref_26, tbb_31, ref_bt11um, ref_01, ref_06)):
        idx_ = np.logical_and.reduce((ref_06 > 29, ref_01 > 24,
                                      np.logical_or(ref_26 > 13.5,
                                                    np.logical_and(ref_26 > 7.5, tbb_31 < ref_bt11um + 8))))
        i_mark[idx_] = 50
        i_step[idx_] = 58
        i_tag[idx_] = 2
        judge[idx_] = False
        del idx_

    # !!!!   Mending TEST For Clear Land  # 原代码也注释了这段代码
    # if no_none((ndvis, tbb_31, dr_16, ndsi_6)):
    #     idx_ = np.logical_and(ndvis > 0.11, tbb_31 < 280)
    #     idx_ = np.logical_or.reduce((idx_, dr_16 < 0, ndsi_6 < -0.15))
    #     idx_ = np.logical_and.reduce((idx_land, judge, idx_))
    #     i_mark[idx_] = 25
    #     i_step[idx_] = 59
    #     i_tag[idx_] = 2
    #     judge[idx_] = False

    if no_none((ndvis, tbb_31)):
        idx_ = np.logical_and.reduce((idx_land, judge, ndvis > 0.11, tbb_31 < 280))
        i_mark[idx_] = 50
        i_step[idx_] = 60
        i_tag[idx_] = 2
        judge[idx_] = False

    if no_none((dr_16, )):
        idx_ = np.logical_and.reduce((idx_land, judge, dr_16 < 0))
        i_mark[idx_] = 25
        i_step[idx_] = 61
        i_tag[idx_] = 2
        judge[idx_] = False

    if no_none((ndsi_6, )):
        idx_ = np.logical_and.reduce((idx_land, judge, ndsi_6 < -0.15))
        i_mark[idx_] = 25
        i_step[idx_] = 62
        i_tag[idx_] = 2
        judge[idx_] = False

    # !!!!   Mending TEST For Clear Land and Cloud by Hai-T11
    if no_none((tbb_31, rr_46)):
        idx_ = np.logical_and(tbb_31 > 280, rr_46 < 1.35)
        idx_ = np.logical_and.reduce((idx_land, judge, idx_))
        i_mark[idx_] = 25
        i_step[idx_] = 66
        i_tag[idx_] = 2
        judge[idx_] = False

    if no_none((tbb_31, ref_dem, ref_01, ref_06, tbb_20, rr_46)):
        idx_ = np.logical_and.reduce((tbb_31 < 280, ref_dem >= 3000, ref_01 >= 40, ref_06 < 20,
                                      tbb_20 < 295, rr_46 > 1.3))
        idx_ = np.logical_and.reduce((idx_land, judge, idx_))
        i_mark[idx_] = 200
        i_step[idx_] = 67
        i_tag[idx_] = 2
        judge[idx_] = False

    if no_none((tbb_31, rr_46, ref_02)):
        idx_ = np.logical_and.reduce((tbb_31 < 280, rr_46 < 1.4, ref_02 < 28))
        idx_ = np.logical_and.reduce((idx_land, judge, idx_))
        i_mark[idx_] = 25
        i_step[idx_] = 68
        i_tag[idx_] = 2
        judge[idx_] = False

    if no_none((tbb_31, rr_46, ref_02)):
        idx_ = np.logical_and.reduce((tbb_31 < 280, rr_46 < 1.4, ref_02 >= 28))
        idx_ = np.logical_and.reduce((idx_land, judge, idx_))
        i_mark[idx_] = 50
        i_step[idx_] = 69
        i_tag[idx_] = 2
        judge[idx_] = False

    # !!!!   UNKNOWN TYPE
    idx_ = np.logical_and.reduce((idx_land, judge))
    i_mark[idx_] = 1
    i_step[idx_] = 99
    i_tag[idx_] = 2
    judge[idx_] = False

    # !!!------------------------------------------------------------------------!!!
    # !!!!    Monthly_SnowPackLine_LUT CLOUD-TEST For The REHANDLED DOT
    # !!!------------------------------------------------------------------------!!!

    # # !!!!  Take Snow-on-Ice Pixel above Water-body as ICE
    # idx_ = np.logical_and.reduce(idx_available, lsm == 0, i_mark == 200)
    # i_mark[idx_] = 100
    # i_step[idx_] = 71
    # del idx_
    #
    # idx_1 = np.logical_and.reduce((idx_available, lsm == 0, i_mark == 1))
    # if ref_02 is not None:
    #     idx_ = np.logical_and(idx_1, ref_02 < 18)
    #     i_mark[idx_] = 39
    #     i_step[idx_] = 72
    #     idx_ = np.logical_and(idx_1, ref_02 > 19)
    #     i_mark[idx_] = 50
    #     i_step[idx_] = 73
    # if ref_26 is not None:
    #     idx_ = np.logical_and(idx_1, ref_26 > 1.5)
    #     i_mark[idx_] = 50
    #     i_step[idx_] = 74
    #
    idx_1 = np.logical_and.reduce((idx_available, lsm == 1, i_mark == 1))
    # judge = np.full(data_shape, True, dtype=np.bool)
    #
    if no_none((ndsi_6, tbb_31, dt_01)):
        idx_ = np.logical_and.reduce((idx_1, ndsi_6 > 0.27, tbb_31 < 273.15, dt_01 > 2.45, dt_01 < 14.10))
        i_mark[idx_] = 200
        i_step[idx_] = 75
        judge[idx_] = False
    #
    # if ref_02 is not None:
    #     idx_ = np.logical_and.reduce((idx_1, judge, ref_02 > 9.1, ref_02 < 26))
    #     i_mark[idx_] = 25
    #     i_step[idx_] = 76
    #
    #     idx_ = np.logical_and.reduce((idx_1, judge, ref_02 > 1.1, ref_02 < 8))
    #     i_mark[idx_] = 25
    #     i_step[idx_] = 77
    #
    #     idx_ = np.logical_and.reduce((idx_1, judge, ref_02 > 46))
    #     i_mark[idx_] = 50
    #     i_step[idx_] = 78
    #
    # if ref_26 is not None:
    #     idx_ = np.logical_and.reduce((idx_1, judge, ref_26 > 10))
    #     i_mark[idx_] = 50
    #     i_step[idx_] = 79
    # del idx_, idx_1, judge

    # !!!==========================================================================!!!
    # !
    # !     SE by Tree-Decision Algorithm after CM
    # !
    # !!!--------------------------------------------------------------------------!!!
    # !!!!   Value = 0 :  Invalid
    # !!!!   Value = 1 :  Coastlines
    # !!!!   Value = 2 :  Uncertain
    # !!!!   Value = 3 :  Cloud
    # !!!!   Value = 4 :  Poss Land Clear
    # !!!!   Value = 5 :  Land Clear
    # !!!!   Value = 6 :  Poss Sea Clear
    # !!!!   Value = 7 :  Sea Clear
    # !!!!   Value = 8 :  Sun Glint
    # !!!--------------------------------------------------------------------------!!!
    if i_cm is not None:
        idx_ = i_cm == 1
        i_mark[idx_] = 240
        i_step[idx_] = 80

        idx_ = np.logical_and.reduce((i_cm <= 2, i_cm >= 3))
        i_mark[idx_] = 50
        i_step[idx_] = 81

        idx_ = np.logical_or.reduce((i_cm == 5, i_cm == 4))
        idx_ = np.logical_and(idx_, i_mark == 1)
        i_mark[idx_] = 25
        i_step[idx_] = 82

        idx_ = np.logical_or.reduce((i_cm == 6,))
        idx_ = np.logical_and(idx_, i_mark == 1)
        i_mark[idx_] = 37
        i_step[idx_] = 83

        idx_ = np.logical_or.reduce((i_cm == 7,))
        idx_ = np.logical_and(idx_, i_mark == 1)
        i_mark[idx_] = 39
        i_step[idx_] = 84

    if DUBUG:
        print('i_mark=', i_mark[row, col])
        print('i_step=', i_step[row, col])
    return i_mark, i_step
