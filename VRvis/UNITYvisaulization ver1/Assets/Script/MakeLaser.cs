using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using ViveSR.anipal.Eye;

public class MakeLaser : MonoBehaviour
{
    public GameObject laserPrefab, EyeRayObj;

    SRanipal_GazeRaySample_v2 rayTest;

    Vector3 start, last;
    GameObject laser;

    void Start()
    {
        rayTest = EyeRayObj.GetComponent<SRanipal_GazeRaySample_v2>();

        laser = Instantiate(laserPrefab);
    }

    void Update()
    {
        start = rayTest.start;
        last = rayTest.last;

        laser.transform.position = Vector3.Lerp(start, last, 0.5f);
        laser.transform.LookAt(last);
        laser.transform.localScale = new Vector3(laser.transform.localScale.x,
            laser.transform.localScale.y, Vector3.Distance(start, last));
    }
}
