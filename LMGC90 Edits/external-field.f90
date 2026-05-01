
!!! ----------- mod_mecaMAILx.f90
              magnitude = (B1**2 + B2**2)**0.5
              if (magnitude .ne. 0) then
              bdir = atan2(B2, B1)
              else
              bdir =0
              end if
              strength = 1


              DO i=1,SIZE(bdyty(ibdyty)%blmty(iblmty)%NODES)
              sin_theta = bdyty(ibdyty)%localFrameIni(2,1)
              cos_theta = bdyty(ibdyty)%localFrameIni(1,1)
              theta = bdyty(ibdyty)%X(3)

              if (magnitude == 0) THEN 
                alignment = 0
              else 
                alignment = (B1*cos_theta + B2*sin_theta) / magnitude ! this is B.m. 1 when aligned, else 0. =cos(angle between). 
              endif

              if ((theta - bdir) >= 0) then ! clockwise rotation
                  DV_ele((i-1)*nbdof+3) = - strength*magnitude*((1-alignment**2)**0.5) ! torque, sin(angle between)
              else if ((theta - bdir) < 0) then ! anticlockwise
                  DV_ele((i-1)*nbdof+3) = strength*magnitude*((1-alignment**2)**0.5) ! torque, sin(angle between)
              endif
          END DO



!!! ----------- mod_RBDY2.f90
             magnitude = (B1**2 + B2**2)**0.5
             if (magnitude .ne. 0) then
             bdir = atan2(B2, B1)
             else
             bdir =0
             end if
             strength = 1

             do iccdof=1,size(bdyty(ibdyty)%V)
             sin_theta = sin(bdyty(ibdyty)%X(3))
             cos_theta = cos(bdyty(ibdyty)%X(3))

              if (magnitude == 0) THEN 
                alignment = 0
              else 
                alignment = (B1*cos_theta + B2*sin_theta) / magnitude
              endif

            !  force(1) = strength*magnitude*sin_theta*(-(1-alignment**2)**0.5) ! sin
            !  force(2) = strength*magnitude*sin_theta*(alignment) ! cos
             if (iccdof == 1) bdyty(ibdyty)%Fext(iccdof)=bdyty(ibdyty)%mass(1)*grav1 !+ force(1)
             if (iccdof == 2) bdyty(ibdyty)%Fext(iccdof)=bdyty(ibdyty)%mass(2)*grav2 !+ force(2)
             if (iccdof == 3) then
                if ((bdyty(ibdyty)%X(3) - bdir)>= 0) then ! clockwise rotation
                    bdyty(ibdyty)%Fext(iccdof)=-strength*magnitude*(1-alignment**2)**0.5
                else if ((bdyty(ibdyty)%X(3) - bdir) < 0) then ! anticlockwise
                    bdyty(ibdyty)%Fext(iccdof)=strength*magnitude*(1-alignment**2)**0.5
                endif
             endif
          end do
          

!!! --------- else: similar formulation, different notation