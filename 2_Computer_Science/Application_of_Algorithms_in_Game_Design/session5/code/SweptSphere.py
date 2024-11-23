#! /usr/bin/env python3
''' Collision Detection: Swept Sphere Demonstrator '''
import pygame
import pygame.locals
import math

def main():
    WINDOW_WIDTH  = 1400
    WINDOW_HEIGHT = 1000

    pygame.init()
    surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('The Swept Sphere Intersection Algorithm')

    thing1  = Thingy(25,              # radius
                     (100, 200),      # Source location
                     (1000, 800),     # Destination location
                     (255, 105, 180), # Source color (Pink)
                     (255, 0, 0),     # Destination color (Red)
                     (250, 128, 114)  # Bounce color (Salmon)
                    )
    thing2  = Thingy(50,              # radius
                     (1100, 300),     # Source location
                     (400, 900),      # Destination location
                     (64, 224, 208),  # Source color (Turquoise)
                     (0, 0, 255),     # Destination color (Blue)
                     (134, 1, 175)    # Bounce color (Violet)
                    )

    events = Controller()
    thing1_collision = thing2_collision = None

    clock = pygame.time.Clock()
    while events.running:
        clock.tick(60)
        events.check_events()

        if not events.running:
            break
        if events.mouse_pressed:
            thing1_collision = thing1.collision(events.mouse_location)
            if not thing1_collision:
                thing2_collision = thing2.collision(events.mouse_location)
        if events.mouse_released:
            if thing1_collision:
                thing1.done_drag(thing1_collision, events.mouse_location)
                thing1_collision = None
            elif thing2_collision:
                thing2.done_drag(thing2_collision, events.mouse_location)
                thing2_collision = None
        if events.mouse_drag:
            if thing1_collision:
                thing1.drag(thing1_collision, events.mouse_location)
            elif thing2_collision:
                thing2.drag(thing2_collision, events.mouse_location)

        thing1.calculate_collision(thing2)
        thing2.calculate_collision(thing1)
        if thing1.is_collision:
            thing1.calculate_bounce(thing2)
            thing2.calculate_bounce(thing1)

        surface.fill((0, 0, 0))
        thing1.draw(surface)
        thing2.draw(surface)
        pygame.display.flip()

class Thingy:
    ''' One circular object, moving through space.  Potentially colliding
        with other such objects.
    '''

    def  __init__(self, radius, src_location, dst_location,
                  color_src, color_dst, color_bounce):
        self.radius = radius
        self.radius_squared = radius * radius
        self.src_location = pygame.math.Vector2(src_location)
        self.dst_location = pygame.math.Vector2(dst_location)
        self.color_src = color_src
        self.color_dst = color_dst
        self.color_bounce = color_bounce
        self.calculate_vectors()
        self.dragging = False

    def calculate_vectors(self):
        self.move_vec = self.dst_location - self.src_location
        self.norm_vec  = pygame.math.Vector2(self.move_vec.y, -self.move_vec.x)
        self.norm_vec.scale_to_length(self.radius)
        self.norm_vec2 = pygame.math.Vector2(-self.move_vec.y, self.move_vec.x)
        self.norm_vec2.scale_to_length(self.radius)

    def collision(self, position):
        ''' Check if the x,y position is inside either the source
            or destination circles.
            Return -- None or 'source' or 'destination'
        '''
        pvec = pygame.math.Vector2(position)
        distance_src = pvec - self.src_location
        if distance_src.length_squared() <= self.radius_squared:
            self.src_location = pygame.math.Vector2(position)
            self.calculate_vectors()
            self.dragging = True
            return 'source'
        distance_dst = pvec - self.dst_location
        if distance_dst.length_squared() <= self.radius_squared:
            self.dst_location = pygame.math.Vector2(position)
            self.calculate_vectors()
            self.dragging = True
            return 'destination'
        return None

    def drag(self, end, position):
        if end == 'source':
            self.src_location = pygame.math.Vector2(position)
            self.calculate_vectors()
        elif end == 'destination':
            self.dst_location = pygame.math.Vector2(position)
            self.calculate_vectors()
        else:
            raise 'Something went very wrong'

    def done_drag(self, end, position):
        self.dragging = False
        if position and end == 'source':
            self.src_location = pygame.math.Vector2(position)
            self.calculate_vectors()
        elif position and end == 'destination':
            self.dst_location = pygame.math.Vector2(position)
            self.calculate_vectors()

    def calculate_collision(self, other_thing):
        ''' Determine the point at which a collision occurs.
            Update internal data to be able to draw the collision properly.
            Using notation from _Game Programming Algorithms and Techniques_
              page 145.
        '''
        vp = self.move_vec
        vq = other_thing.move_vec

        # Calculate A and B
        # A = P0 - Q0
        A = self.src_location - other_thing.src_location
        # B = vp - vq
        B = vp - vq

        # Calculate a, b and c (coefficients of quadratic equation)
        # a = B dot B
        a = B.dot(B)
        # b = 2(A dot B)
        b = 2 * A.dot(B)
        # c = (A dot A) - (rp + rq) * (rp + rq)
        c = A.dot(A) - (self.radius + other_thing.radius)**2

        # Calculate the discriminant
        disc = b**2 - 4 * a * c
        if disc > 0:
            t = (-b - math.sqrt(disc)) / (2 * a)
            if t > 0 and t <=1:
                self.is_collision = True
                length = self.move_vec.length() * t
                if length < 1:
                    length = 1
                self.collision_vec = pygame.math.Vector2(self.move_vec)
                self.collision_vec.scale_to_length(length)
            else:
                self.is_collision = False
        elif disc == 0:
            print('Tangent touch')
        else:
            self.is_collision = False

    def calculate_bounce(self, other_thing):
        ''' A collision has been detected.  The location of that vector is
            self.collision_vec + self.src_location.  Bounce off of the plane
            tangentially normal to the circle in the direction of other_thing's
            collision location.
        '''
        collision_point_mycenter = self.collision_vec + self.src_location
        collision_point_othercenter = other_thing.collision_vec + other_thing.src_location
        bounce_plane_normal = collision_point_mycenter - collision_point_othercenter
        self.bounce_vec = self.collision_vec.reflect(bounce_plane_normal)
        motion_total = self.move_vec.length()
        motion_before = self.collision_vec.length()
        motion_after = motion_total - motion_before
        if motion_after < 1:
            motion_after = 1
        self.bounce_vec.scale_to_length(motion_after)

    def draw(self, surface):
        circle_width = 10
        line_width = 3
        pygame.draw.line(surface, (180,180,180),
                         self.src_location + self.norm_vec,
                         self.dst_location + self.norm_vec)
        pygame.draw.line(surface, (180,180,180),
                         self.src_location + self.norm_vec2,
                         self.dst_location + self.norm_vec2)
        pygame.draw.circle(surface, self.color_src, self.src_location,
                           self.radius, width=circle_width)
        pygame.draw.circle(surface, self.color_dst, self.dst_location,
                           self.radius, width=circle_width)
        if self.is_collision:
            pygame.draw.circle(surface, self.color_bounce,
                               self.src_location + self.collision_vec,
                               self.radius, width=circle_width)
            pygame.draw.circle(surface, self.color_bounce,
                               self.src_location + self.collision_vec + self.bounce_vec,
                               self.radius, width=circle_width)
            pygame.draw.line(surface, (0,200,50),
                         self.src_location,
                         self.src_location + self.collision_vec,
                         width = line_width)
            pygame.draw.line(surface, self.color_bounce,
                             self.src_location + self.collision_vec,
                             self.src_location + self.collision_vec + self.bounce_vec,
                             width = line_width)

class Controller:

    def __init__(self):
        self.running = True
        self.mouse_drag = False    # Is the mouse currently being dragged?
        self.mouse_pressed  = False
        self.mouse_released = False
        self.mouse_location = None

    def check_events(self):
        self.mouse_pressed  = False  # Mouse data good for only one frame
        self.mouse_released = False

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_pressed = True
                self.mouse_drag = True
                self.mouse_location = event.pos
            if event.type == pygame.MOUSEBUTTONUP:
                self.mouse_released = True
                self.mouse_drag = False
                self.mouse_location = event.pos
            if event.type == pygame.MOUSEMOTION:
                if self.mouse_drag:
                    self.mouse_location = event.pos
                else:
                    self.mouse_location = None

if __name__ == "__main__":
    main()